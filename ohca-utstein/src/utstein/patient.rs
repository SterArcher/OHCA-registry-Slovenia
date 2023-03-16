use bigdecimal::ToPrimitive;
use serde::Serialize;
use sqlx::MySqlPool;

#[derive(Debug, Serialize)]
pub struct Patient {
    pub age: Age,
    pub sex: Sex,
}

impl Patient {
    pub async fn new(pool: &MySqlPool) -> Self {
        Self {
            age: Age::new(pool).await,
            sex: Sex::new(pool).await,
        }
    }
}

#[derive(Debug, Serialize)]
pub struct Age {
    pub mean: f64,
    pub unknown: i64,
    pub standard_deviation: f64,
}

impl Age {
    pub async fn new(pool: &MySqlPool) -> Self {
        let record = sqlx::query!(
            r#"
                SELECT
                    AVG(age) AS mean,
                    (SELECT COUNT(*) FROM cases WHERE age IS NULL) AS "unknown!",
                    STD(age) AS standard_deviation
                FROM cases;
            "#
        )
        .fetch_one(pool)
        .await
        .unwrap();

        Self {
            mean: record.mean.unwrap().to_f64().unwrap(),
            unknown: record.unknown,
            standard_deviation: record.standard_deviation.unwrap().to_f64().unwrap(),
        }
    }
}

#[derive(Debug, Serialize)]
pub struct Sex {
    pub male: i64,
    pub female: i64,
    pub unknown: i64,
}

impl Sex {
    pub async fn new(pool: &MySqlPool) -> Self {
        sqlx::query_as!(
            Sex,
            r#"
                SELECT
                    (SELECT COUNT(*) FROM cases WHERE gender = 0) AS "male!: i64",
                    (SELECT COUNT(*) FROM cases WHERE gender = 1) AS "female!: i64",
                    (SELECT COUNT(*) FROM cases WHERE gender = -1 OR gender IS NULL) AS "unknown!: i64"
            "#
        )
        .fetch_one(pool)
        .await
        .unwrap()
    }
}
