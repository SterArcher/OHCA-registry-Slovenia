use bigdecimal::ToPrimitive;
use serde::Serialize;
use sqlx::MySqlPool;

use crate::utils::confidence_interval_90;

/// The core fields of the report
///
/// # Field mappings
///
/// * Population served - `population_served` is the sum of the `population` column from the `systems` table
/// * Cardiac arrests attended - `cardiac_arrests_attended` is the sum of the `attendedCAs` column from the `systems` table
/// * Response time - `response_time` formatted in `mm:ss ± mm:ss` is a string representation of the 90% confidence interval of the `responseTime` column from the `cases` table
#[derive(Debug, Serialize)]
pub struct Core {
    pub population_served: i64,
    pub cardiac_arrests_attended: i64,
    pub response_time: String,
}

impl Core {
    /// Generates a new Core struct
    ///
    /// # Arguments
    ///
    /// * `pool` - The `MySqlPool` connection pool for database.
    pub async fn new(pool: &MySqlPool) -> Self {
        // The mean and standard deviation are calculated in the database. They could also be calculated
        // in code, but this saves a bit of hassle and doesn't require you to return the values of the entire column.
        let record = sqlx::query!(
            r#"
                SELECT 
                    (SELECT SUM(population) FROM systems) AS population_served,
                    (SELECT SUM(attendedCAs) FROM systems) AS cardiac_arrests_attended,
                    (SELECT AVG(responseTime) FROM cases WHERE responseTime IS NOT NULL) AS response_time_mean,
                    (SELECT STD(responseTime) FROM cases WHERE responseTime IS NOT NULL) AS response_time_std,
                    (SELECT COUNT(*)) as count
            "#
        )
        .fetch_one(pool)
        .await
        .unwrap();

        // Calculate the confidence interval in seconds
        let mean = record.response_time_mean.unwrap().to_f64().unwrap();
        let std = record.response_time_std.unwrap().to_f64().unwrap();
        let response_time_ci = confidence_interval_90(record.count, mean, std);

        // Convert the response time from seconds into minutes and seconds
        let dur_min = (response_time_ci.0 / 60.).floor() as i64;
        let dur_sec = (response_time_ci.0 % 60.).ceil() as i64;

        // Convert the error of the response time from seconds into minutes and seconds
        let error_min = (response_time_ci.1 / 60.).floor() as i64;
        let error_sec = (response_time_ci.1 % 60.).ceil() as i64;

        Self {
            // Using SUM in SQLx returns a BigDecimal type, which should be safe to unwrap.
            population_served: record.population_served.unwrap().to_i64().unwrap(),
            cardiac_arrests_attended: record.cardiac_arrests_attended.unwrap().to_i64().unwrap(),
            response_time: format!("{dur_min}:{dur_sec} ± {error_min}:{error_sec}"),
        }
    }
}
