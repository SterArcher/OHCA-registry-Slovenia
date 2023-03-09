use bigdecimal::ToPrimitive;
use serde::Serialize;
use sqlx::MySqlPool;

use crate::utils::confidence_interval_90;

/// The Utstein report template
#[derive(Debug, Serialize)]
pub struct Utstein {
    pub system_core: Core,
    pub dispatcher_id_ca: DispatcherIdCA,
    pub dispatcher_cpr: DispatcherCPR,
    pub resc_attempted: RescAttempted,
    pub resc_not_attempted: RescNotAttempted,
    pub location: Location,
    pub patient: Patient,
    pub witnessed: Witnessed,
    pub bystander_response: BystanderResponse,
    pub etiology: Etiology,
    pub ems_process: EMSProcess,
    pub hospital_process: HospitalProcess,
    pub patient_outcomes: PatientOutcomes,
}

impl Utstein {
    /// Creates a new Utstein report given a database connection pool
    ///
    /// # Arguments
    ///
    /// * `pool` - The `MySqlPool` connection pool for database
    pub async fn new(pool: &MySqlPool) -> Self {
        Self {
            system_core: Core::new(pool).await,
            dispatcher_id_ca: DispatcherIdCA::new(pool).await,
            dispatcher_cpr: DispatcherCPR::new(pool).await,
            resc_attempted: RescAttempted::new(pool).await,
            resc_not_attempted: RescNotAttempted::new(pool).await,
            location: Location::new(pool).await,
            patient: Patient::new(pool).await,
            witnessed: Witnessed::new(pool).await,
            bystander_response: BystanderResponse::new(pool).await,
            etiology: Etiology::new(pool).await,
            ems_process: EMSProcess::new(pool).await,
            hospital_process: HospitalProcess::new(pool).await,
            patient_outcomes: PatientOutcomes::new(pool).await,
        }
    }
}

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
    async fn new(pool: &MySqlPool) -> Self {
        // The mean and standard deviation are calculated in the database. They could also be calculated
        // in code, but this saves a bit of hassle and doesn't require you to return the values of the entire column.
        let record = sqlx::query!(
            r#"
                SELECT 
                    (SELECT SUM(population) AS "population_served!: i64" FROM systems) AS population_served,
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

/// The Dispatcher ID CA (Dispatcher Identified Cardiac Arrests) field
///
/// # Field mappings
///
/// * Yes - `yes` is the number of rows where `dispIdentifiedCA` = 1
/// * No - `no` is the number of rows where `dispIdentifiedCA` = 0
/// * Unknown - `unknown` is the number of rows where `dispIdentifiedCA` is -1 or NULL
#[derive(Debug, Serialize)]
pub struct DispatcherIdCA {
    pub yes: i64,
    pub no: i64,
    pub unknown: i64,
}

impl DispatcherIdCA {
    /// Generates a new DispatcherIdCA struct
    ///
    /// # Arguments
    ///
    /// * `pool` - The `MySqlPool` connection pool for database.
    async fn new(pool: &MySqlPool) -> Self {
        // using the `sqlx::query_as!` you can specify what the output type the query should return
        // so we don't need to do any explicit mapping of the columns
        sqlx::query_as!(
            DispatcherIdCA,
            r#"
                SELECT
                    (SELECT COUNT(*) FROM cases WHERE dispIdentifiedCA = 1) AS "yes!: i64",
                    (SELECT COUNT(*) FROM cases WHERE dispIdentifiedCA = 0) AS "no!: i64",
                    (SELECT COUNT(*) FROM cases WHERE dispIdentifiedCA = -1 OR dispProvidedCprinst IS NULL) AS "unknown!: i64"
            "#
        )
        .fetch_one(pool)
        .await
        .unwrap()
    }
}

/// The Dispatcher CPR (Dispatcher provided CPR instructions) field
///
/// # Field mappings
///
/// * Yes - `yes` is the number of rows where `dispProvidedCPRinst` = 1
/// * No - `no` is the number of rows where `dispProvidedCPRinst` = 0
/// * Unknown - `unknown` is the number of rows where `dispProvidedCPRinst` is -1 or NULL
#[derive(Debug, Serialize)]
pub struct DispatcherCPR {
    pub yes: i64,
    pub no: i64,
    pub unknown: i64,
}

impl DispatcherCPR {
    /// Generates a new DispatcherCPR struct
    ///
    /// # Arguments
    ///
    /// * `pool` - The `MySqlPool` connection pool for database.
    async fn new(pool: &MySqlPool) -> Self {
        sqlx::query_as!(
            DispatcherCPR,
            r#"
                SELECT
                    (SELECT COUNT(*) FROM cases WHERE dispProvidedCPRinst = 1) AS "yes!: i64",
                    (SELECT COUNT(*) FROM cases WHERE dispProvidedCPRinst = 0) AS "no!: i64",
                    (SELECT COUNT(*) FROM cases WHERE dispProvidedCPRinst = -1 OR dispProvidedCprinst IS NULL) AS "unknown!: i64"
            "#
        )
        .fetch_one(pool)
        .await
        .unwrap()
    }
}

/// The Resuscitation Attempted field
///
/// Filters all the cases, with the following filters:
///
/// * `bystanedResponse` is 1 or 2,
/// * or `bystanderAED` is 1 or 2,
/// * or `mechanicalCPR` is 1, 2 or 3.
///
/// # Field mappings
///
/// * VF - `vf` is the number of rows where `firstMonitoredRhy` = 1
/// * VT - `vt` is the number of rows where `firstMonitoredRhy` = 2
/// * PEA - `pea` is the number of rows where `firstMonitoredRhy` = 3
/// * ASYS - `asys` is the number of rows where `firstMonitoredRhy` = 4
/// * Brady - `brady` is the number of rows where `firstMonitoredRhy` = 5
/// * AED Non-shockable - `aed_non_shockable` is the number of rows where `firstMonitoredRhy` = 6
/// * AED Shockable - `aed_shockable` is the number of rows where `firstMonitoredRhy` = 7
/// * Not recorded - `not_recorded` is the number of rows where `firstMonitoredRhy` is NULL
/// * Unknown - `unknown` is the number of rows where `firstMonitoredRhy` is -1
#[derive(Debug, Serialize)]
pub struct RescAttempted {
    pub vf: i64,
    pub vt: i64,
    pub pea: i64,
    pub asys: i64,
    pub brady: i64,
    pub aed_non_shockable: i64,
    pub aed_shockable: i64,
    pub not_recorded: i64,
    pub unknown: i64,
}

impl RescAttempted {
    /// Generates a new RescAttempted struct
    ///
    /// # Arguments
    ///
    /// * `pool` - The `MySqlPool` connection pool for database.
    async fn new(pool: &MySqlPool) -> Self {
        // Query with a common table expression - CTE
        // Read more at https://mariadb.com/kb/en/with/

        // First create a temporary table, where the only columns is `firstMonitorRhy`
        // Then get results from that table according to the required filter
        sqlx::query_as!(
            RescAttempted,
            r#"
                WITH rescucitaion AS 
                (
                    SELECT
                        firstMonitoredRhy
                    FROM cases
                    WHERE bystanderResponse BETWEEN 1 AND 2
                    OR bystanderAED BETWEEN 1 AND 2
                    OR mechanicalCPR BETWEEN 1 AND 3
                )
                SELECT
                    (SELECT COUNT(*) FROM rescucitaion WHERE firstMonitoredRhy = 1) AS "vf!: i64",
                    (SELECT COUNT(*) FROM rescucitaion WHERE firstMonitoredRhy = 2) AS "vt!: i64",
                    (SELECT COUNT(*) FROM rescucitaion WHERE firstMonitoredRhy = 3) AS "pea!: i64",
                    (SELECT COUNT(*) FROM rescucitaion WHERE firstMonitoredRhy = 4) AS "asys!: i64",
                    (SELECT COUNT(*) FROM rescucitaion WHERE firstMonitoredRhy = 5) AS "brady!: i64",
                    (SELECT COUNT(*) FROM rescucitaion WHERE firstMonitoredRhy = 6) AS "aed_non_shockable!: i64",
                    (SELECT COUNT(*) FROM rescucitaion WHERE firstMonitoredRhy = 7) AS "aed_shockable!: i64",
                    (SELECT COUNT(*) FROM rescucitaion WHERE firstMonitoredRhy IS NULL) AS "not_recorded!: i64",
                    (SELECT COUNT(*) FROM rescucitaion WHERE firstMonitoredRhy = -1) AS "unknown!: i64"
            "#
        )
        .fetch_one(pool)
        .await
        .unwrap()
    }
}

/// The Resuscitation Not Attempted field
///
/// # Field mappings
///
/// * All Cases - `all_cases` is the difference of the sum of the columns `attendedCAs` and `attemptedResusc` from the `systems` table
/// * DNAR (Did not attempt resuscitation) - `dnar` is the sum of the column `casesDNR` from the `systems` table
/// * Obviously dead - `obviously_dead` is the number of rows where `deadOnArrival` = 1 from the `cases` table
/// * Signs of Life - `signs_of_life` is the sum of the column `casesCirculation` from the `systems` table
#[derive(Debug, Serialize)]
pub struct RescNotAttempted {
    pub all_cases: i64,
    pub dnar: i64,
    pub obviously_dead: i64,
    pub signs_of_life: i64,
}

impl RescNotAttempted {
    /// Generates a new RescNotAttempted struct
    ///
    /// # Arguments
    ///
    /// * `pool` - The `MySqlPool` connection pool for database.
    async fn new(pool: &MySqlPool) -> Self {
        let record = sqlx::query!(
            r#"
                SELECT
                    (SELECT SUM(attendedCAs) - SUM(attemptedResusc) FROM systems) AS all_cases,
                    (SELECT SUM(casesDNR) FROM systems) AS dnar,
                    (SELECT COUNT(*) FROM cases WHERE deadOnArrival = 1) AS obviously_dead,
                    (SELECT SUM(casesCirculation) FROM systems) AS signs_of_life
            "#
        )
        .fetch_one(pool)
        .await
        .unwrap();

        Self {
            all_cases: record.all_cases.unwrap().to_i64().unwrap(),
            dnar: record.dnar.unwrap().to_i64().unwrap(),
            obviously_dead: record.obviously_dead.unwrap().to_i64().unwrap(),
            signs_of_life: record.signs_of_life.unwrap().to_i64().unwrap(),
        }
    }
}

#[derive(Debug, Serialize)]
pub struct Location {
    pub home: i64,
    pub work: i64,
    pub rec: i64,
    pub public: i64,
    pub educ: i64,
    pub nursing: i64,
    pub other: i64,
    pub unknown: i64,
}
//7 and 6 are switched
impl Location {
    async fn new(pool: &MySqlPool) -> Self {
        sqlx::query_as!(
            Location,
            r#"
                SELECT
                    (SELECT COUNT(*) FROM cases WHERE location = 0) AS "home!: i64",
                    (SELECT COUNT(*) FROM cases WHERE location = 1) AS "work!: i64",
                    (SELECT COUNT(*) FROM cases WHERE location = 2) AS "rec!: i64",
                    (SELECT COUNT(*) FROM cases WHERE location = 4) AS "public!: i64",
                    (SELECT COUNT(*) FROM cases WHERE location = 6) AS "educ!: i64",
                    (SELECT COUNT(*) FROM cases WHERE location = 5) AS "nursing!: i64",
                    (SELECT COUNT(*) FROM cases WHERE location = 7) AS "other!: i64",
                    (SELECT COUNT(*) FROM cases WHERE location = -1 OR location IS NULL) AS "unknown!: i64"
            "#
        )
        .fetch_one(pool)
        .await
        .unwrap()
    }
}

#[derive(Debug, Serialize)]
pub struct Patient {
    pub age: Age,
    pub sex: Sex,
}

impl Patient {
    async fn new(pool: &MySqlPool) -> Self {
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
    async fn new(pool: &MySqlPool) -> Self {
        let record = sqlx::query!(
            r#"
                SELECT
                    AVG(age) AS mean,
                    (SELECT COUNT(*) FROM cases WHERE age IS NULL) AS "unknown!: i64"
                    STD(age) AS standard_deviation,
                FROM cases
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
    async fn new(pool: &MySqlPool) -> Self {
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

#[derive(Debug, Serialize)]
pub struct Witnessed {
    pub bystander: i64,
    pub ems: i64,
    pub unwitnessed: i64,
    pub unknown: i64,
}

impl Witnessed {
    async fn new(pool: &MySqlPool) -> Self {
        sqlx::query_as!(
            Witnessed,
            r#"
                SELECT
                    (SELECT COUNT(*) FROM cases WHERE witnesses = 1) AS "bystander!: i64",
                    (SELECT COUNT(*) FROM cases WHERE witnesses = 2) AS "ems!: i64",
                    (SELECT COUNT(*) FROM cases WHERE witnesses = 0) AS "unwitnessed!: i64",
                    (SELECT COUNT(*) FROM cases WHERE witnesses = -1 OR bystanderResponse IS NULL) AS "unknown!: i64"
            "#
        )
        .fetch_one(pool)
        .await
        .unwrap()
    }
}

#[derive(Debug, Serialize)]
pub struct BystanderResponse {
    pub bystander_cpr: BystanderCPR,
    pub bystander_aed: BystanderAED,
}

impl BystanderResponse {
    async fn new(pool: &MySqlPool) -> Self {
        Self {
            bystander_cpr: BystanderCPR::new(pool).await,
            bystander_aed: BystanderAED::new(pool).await,
        }
    }
}

#[derive(Debug, Serialize)]
pub struct BystanderCPR {
    pub no_bcpr: i64,
    pub bcpr: i64,
    pub cc_only: i64,
    pub cc_or_vent: i64,
    pub unknown: i64,
}

impl BystanderCPR {
    async fn new(pool: &MySqlPool) -> Self {
        sqlx::query_as!(
            BystanderCPR,
            r#"
                SELECT
                    (SELECT COUNT(*) FROM cases WHERE bystanderResponse = 0) AS "no_bcpr!: i64",
                    (SELECT COUNT(*) FROM cases WHERE bystanderResponse = 1) AS "cc_only!: i64",
                    (SELECT COUNT(*) FROM cases WHERE bystanderResponse = 2) AS "cc_or_vent!: i64",
                    (SELECT COUNT(*) FROM cases WHERE bystanderResponse BETWEEN 1 AND 2) AS "bcpr!: i64",
                    (SELECT COUNT(*) FROM cases WHERE bystanderResponse = -1 OR bystanderResponse IS NULL) AS "unknown!: i64"
            "#
        )
        .fetch_one(pool)
        .await
        .unwrap()
    }
}

#[derive(Debug, Serialize)]
pub struct BystanderAED {
    pub analyse: i64,
    pub shock: i64,
    pub unknown: i64,
}

impl BystanderAED {
    async fn new(pool: &MySqlPool) -> Self {
        sqlx::query_as!(
            BystanderAED,
            r#"
                SELECT
                    (SELECT COUNT(*) FROM cases WHERE bystanderAED = 1) AS "analyse!: i64",
                    (SELECT COUNT(*) FROM cases WHERE bystanderAED = 2) AS "shock!: i64",
                    (SELECT COUNT(*) FROM cases WHERE bystanderAED = -1) AS "unknown!: i64"
            "#
        )
        .fetch_one(pool)
        .await
        .unwrap()
    }
}

#[derive(Debug, Serialize)]
pub struct Etiology {
    pub medical: i64,
    pub trauma: i64,
    pub overdose: i64,
    pub drowning: i64,
    pub electrocution: i64,
    pub asphyxial: i64,
    pub not_recorded: i64,
}

impl Etiology {
    async fn new(pool: &MySqlPool) -> Self {
        sqlx::query_as!(
            Etiology,
            r#"
                SELECT
                    (SELECT COUNT(*) FROM cases WHERE pathogenesis = 1) AS "medical!: i64",
                    (SELECT COUNT(*) FROM cases WHERE pathogenesis = 2) AS "trauma!: i64",
                    (SELECT COUNT(*) FROM cases WHERE pathogenesis = 3) AS "overdose!: i64",
                    (SELECT COUNT(*) FROM cases WHERE pathogenesis = 4) AS "drowning!: i64",
                    (SELECT COUNT(*) FROM cases WHERE pathogenesis = 5) AS "electrocution!: i64",
                    (SELECT COUNT(*) FROM cases WHERE pathogenesis = 6) AS "asphyxial!: i64",
                    (SELECT COUNT(*) FROM cases WHERE pathogenesis IS NULL) AS "not_recorded!: i64"
            "#
        )
        .fetch_one(pool)
        .await
        .unwrap()
    }
}

#[derive(Debug, Serialize)]
pub struct EMSProcess {
    pub first_defib_time: f64,

    // targeted temp control
    pub indicated_done: i64,
    pub indicated_not_done: i64,
    pub not_indicated: i64,
    pub unknown: i64,

    // drugs given
    pub drugs_given: i64,
}

impl EMSProcess {
    async fn new(pool: &MySqlPool) -> Self {
        let record = sqlx::query!(
            r#"
                SELECT
                    (SELECT AVG(defibTime) FROM cases WHERE defibTime IS NOT NULL OR defibTime != -1) AS first_defib_time,
                    (SELECT COUNT(*) FROM cases WHERE ttm BETWEEN 1 AND 3) AS "indicated_done!: i64",
                    (SELECT COUNT(*) FROM cases WHERE ttm = 4) AS "indicated_not_done!: i64",
                    (SELECT COUNT(*) FROM cases WHERE ttm = 5) AS "not_indicated!: i64",
                    (SELECT COUNT(*) FROM cases WHERE ttm = -1 OR ttm IS NULL) AS "unknown!: i64",
                    (SELECT COUNT(*) FROM cases WHERE drugs IS NOT NULL OR drugs != -1) AS "drugs_given!: i64"
            "#
        ).fetch_one(pool)
        .await
        .unwrap();

        Self {
            first_defib_time: record.first_defib_time.unwrap().to_f64().unwrap(),
            indicated_done: record.indicated_done,
            indicated_not_done: record.indicated_not_done,
            not_indicated: record.not_indicated,
            unknown: record.unknown,
            drugs_given: record.drugs_given,
        }
    }
}

#[derive(Debug, Serialize)]
pub struct HospitalProcess {
    // reperfusion
    pub attempted: i64,

    // targeted temp control
    pub indicated_done: i64,
    pub indicated_not_done: i64,
    pub not_indicated: i64,
    pub unknown: i64,

    // organ donation
    pub organ_donation: i64,
}

impl HospitalProcess {
    async fn new(pool: &MySqlPool) -> Self {
        sqlx::query_as!(
            HospitalProcess,
            r#"
                SELECT
                    (SELECT COUNT(*) FROM cases WHERE reperfusionAttempt IS NOT NULL OR reperfusionAttempt != -1) AS "attempted!: i64",
                    (SELECT COUNT(*) FROM cases WHERE ttm BETWEEN 1 AND 3) AS "indicated_done!: i64",
                    (SELECT COUNT(*) FROM cases WHERE ttm = 4) AS "indicated_not_done!: i64",
                    (SELECT COUNT(*) FROM cases WHERE ttm = 5) AS "not_indicated!: i64",
                    (SELECT COUNT(*) FROM cases WHERE ttm = -1 OR ttm IS NULL) AS "unknown!: i64",
                    (SELECT COUNT(*) FROM cases WHERE organDonation = 1) AS "organ_donation!: i64"
            "#
        ).fetch_one(pool)
        .await
        .unwrap()
    }
}

#[derive(Debug, Serialize)]
pub struct PatientOutcomes {
    pub all_ems_treated_arrests: Columns,
    pub ems_witnessed_excluded: EmsWitnessedExcluded,
}

impl PatientOutcomes {
    async fn new(pool: &MySqlPool) -> Self {
        // TODO: which fields are required for this
        let all_ems_treated_arrests = Columns {
            any_rosc_yes: 0,
            any_rosc_unknown: 0,
            survived_event_yes: 0,
            survived_event_unknown: 0,
            survival_30d_yes: 0,
            survival_30d_unknown: 0,
            fav_neurological_yes: 0,
            fav_neurological_unknown: 0,
        };

        // let all_ems_treated_arrests = sqlx::query_as!(
        //     Columns,
        //     r#"
        //         WITH witness_included AS
        //         (
        //             SELECT
        //                 witnesses,
        //                 rosc,
        //                 survivalStatus,
        //                 SurvivalDischarge30d,
        //                 mrsDischarge,
        //                 cpcDischarge
        //             FROM cases
        //             WHERE bystanderResponse BETWEEN 1 AND 2
        //             OR bystanderAED BETWEEN 1 AND 2
        //             OR mechanicalCPR BETWEEN 1 AND 3
        //             AND witnesses BETWEEN 2 AND 3
        //         )
        //         SELECT
        //             (SELECT COUNT(*) FROM witness_included WHERE rosc = 1) AS "any_rosc_yes!: i64",
        //             (SELECT COUNT(*) FROM witness_included WHERE rosc = -1 OR rosc IS NULL) AS "any_rosc_unknown!: i64",
        //             (SELECT COUNT(*) FROM witness_included WHERE survivalStatus = 1) AS "survived_event_yes!: i64",
        //             (SELECT COUNT(*) FROM witness_included WHERE survivalStatus = -1 OR survivalStatus IS NULL) AS "survived_event_unknown!: i64",
        //             (SELECT COUNT(*) FROM witness_included WHERE SurvivalDischarge30d = 1) AS "survival_30d_yes!: i64",
        //             (SELECT COUNT(*) FROM witness_included WHERE SurvivalDischarge30d = -1 OR SurvivalDischarge30d IS NULL) AS "survival_30d_unknown!: i64",
        //             (SELECT COUNT(*) FROM witness_included WHERE mrsDischarge = 3 OR cpcDischarge = 2) AS "fav_neurological_yes!: i64",    -- TODO preveri
        //             (SELECT COUNT(*) FROM witness_included WHERE mrsDischarge = -1 OR mrsDischarge IS NULL) AS "fav_neurological_unknown!: i64"
        //     "#
        // ).fetch_one(pool)
        // .await
        // .unwrap();

        Self {
            all_ems_treated_arrests,
            ems_witnessed_excluded: EmsWitnessedExcluded::new(pool).await,
        }
    }
}

#[derive(Debug, Serialize)]
pub struct EmsWitnessedExcluded {
    pub shockable_bystander_witnessed: Columns,
    pub shockable_bystander_cpr: Columns,
    pub non_shockable_witnessed: Columns,
}

impl EmsWitnessedExcluded {
    async fn new(pool: &MySqlPool) -> Self {
        let shockable_bystander_witnessed = sqlx::query_as!(
            Columns,
            r#"
                WITH witness_included AS 
                (
                    SELECT
                        witnesses,
                        rosc,
                        survivalStatus,
                        SurvivalDischarge30d,
                        mrsDischarge,
                        cpcDischarge
                    FROM cases
                    WHERE bystanderResponse BETWEEN 1 AND 2
                    OR bystanderAED BETWEEN 1 AND 2
                    OR mechanicalCPR BETWEEN 1 AND 3
                    AND witnesses BETWEEN 2 AND 3
                )
                SELECT
                    (SELECT COUNT(*) FROM witness_included WHERE rosc = 1) AS "any_rosc_yes!: i64",
                    (SELECT COUNT(*) FROM witness_included WHERE rosc = -1 OR rosc IS NULL) AS "any_rosc_unknown!: i64",
                    (SELECT COUNT(*) FROM witness_included WHERE survivalStatus = 1) AS "survived_event_yes!: i64",
                    (SELECT COUNT(*) FROM witness_included WHERE survivalStatus = -1 OR survivalStatus IS NULL) AS "survived_event_unknown!: i64",
                    (SELECT COUNT(*) FROM witness_included WHERE SurvivalDischarge30d = 1) AS "survival_30d_yes!: i64",
                    (SELECT COUNT(*) FROM witness_included WHERE SurvivalDischarge30d = -1 OR SurvivalDischarge30d IS NULL) AS "survival_30d_unknown!: i64",
                    (SELECT COUNT(*) FROM witness_included WHERE mrsDischarge = 3 OR cpcDischarge = 2) AS "fav_neurological_yes!: i64",    -- TODO preveri
                    (SELECT COUNT(*) FROM witness_included WHERE mrsDischarge = -1 OR mrsDischarge IS NULL) AS "fav_neurological_unknown!: i64"
            "#
        ).fetch_one(pool)
        .await
        .unwrap();

        let shockable_bystander_cpr = sqlx::query_as!(
            Columns,
            r#"
                WITH witness_excluded AS 
                (
                    SELECT
                        witnesses,
                        rosc,
                        survivalStatus,
                        SurvivalDischarge30d,
                        mrsDischarge,
                        cpcDischarge
                    FROM cases
                    WHERE bystanderResponse BETWEEN 1 AND 2
                    OR bystanderAED BETWEEN 1 AND 2
                    OR mechanicalCPR BETWEEN 1 AND 3
                    AND witnesses = 2
                    AND bystanderResponse = 0   -- TODO: bystander response is between 1 and 2, but also has to be 0?
                    AND firstMonitoredRhy = 7
                )
                SELECT
                    (SELECT COUNT(*) FROM witness_excluded WHERE rosc = 1) AS "any_rosc_yes!: i64",
                    (SELECT COUNT(*) FROM witness_excluded WHERE rosc = -1 OR rosc IS NULL) AS "any_rosc_unknown!: i64",
                    (SELECT COUNT(*) FROM witness_excluded WHERE survivalStatus = 1) AS "survived_event_yes!: i64",
                    (SELECT COUNT(*) FROM witness_excluded WHERE survivalStatus = -1 OR survivalStatus IS NULL) AS "survived_event_unknown!: i64",
                    (SELECT COUNT(*) FROM witness_excluded WHERE SurvivalDischarge30d = 1) AS "survival_30d_yes!: i64",
                    (SELECT COUNT(*) FROM witness_excluded WHERE SurvivalDischarge30d = -1 OR SurvivalDischarge30d IS NULL) AS "survival_30d_unknown!: i64",
                    (SELECT COUNT(*) FROM witness_excluded WHERE mrsDischarge = 3 OR cpcDischarge = 2) AS "fav_neurological_yes!: i64",                     -- todo narobe
                    (SELECT COUNT(*) FROM witness_excluded WHERE mrsDischarge = -1 OR mrsDischarge IS NULL) AS "fav_neurological_unknown!: i64"
            "#
        ).fetch_one(pool)
        .await
        .unwrap();

        let non_shockable_witnessed = sqlx::query_as!(
            Columns,
            r#"
                WITH witness_excluded AS 
                (
                    SELECT
                        witnesses,
                        rosc,
                        survivalStatus,
                        SurvivalDischarge30d,
                        mrsDischarge,
                        cpcDischarge
                    FROM cases
                    WHERE bystanderResponse BETWEEN 1 AND 2
                    OR bystanderAED BETWEEN 1 AND 2
                    OR mechanicalCPR BETWEEN 1 AND 3
                    AND witnesses = 2
                    AND bystanderResponse = 0   -- TODO: bystander response is between 1 and 2, but also has to be 0?
                    AND firstMonitoredRhy = 6
                )
                SELECT
                    (SELECT COUNT(*) FROM witness_excluded WHERE rosc = 1) AS "any_rosc_yes!: i64",
                    (SELECT COUNT(*) FROM witness_excluded WHERE rosc = -1 OR rosc IS NULL) AS "any_rosc_unknown!: i64",
                    (SELECT COUNT(*) FROM witness_excluded WHERE survivalStatus = 1) AS "survived_event_yes!: i64",
                    (SELECT COUNT(*) FROM witness_excluded WHERE survivalStatus = -1 OR survivalStatus IS NULL) AS "survived_event_unknown!: i64",
                    (SELECT COUNT(*) FROM witness_excluded WHERE SurvivalDischarge30d = 1) AS "survival_30d_yes!: i64",
                    (SELECT COUNT(*) FROM witness_excluded WHERE SurvivalDischarge30d = -1 OR SurvivalDischarge30d IS NULL) AS "survival_30d_unknown!: i64",
                    (SELECT COUNT(*) FROM witness_excluded WHERE mrsDischarge = 3 OR cpcDischarge = 2) AS "fav_neurological_yes!: i64",                     -- todo narobe
                    (SELECT COUNT(*) FROM witness_excluded WHERE mrsDischarge = -1 OR mrsDischarge IS NULL) AS "fav_neurological_unknown!: i64"
            "#
        ).fetch_one(pool)
        .await
        .unwrap();

        Self {
            shockable_bystander_witnessed,
            shockable_bystander_cpr,
            non_shockable_witnessed,
        }
    }
}

#[derive(Debug, Serialize)]
pub struct Columns {
    pub any_rosc_yes: i64,
    pub any_rosc_unknown: i64,
    pub survived_event_yes: i64,
    pub survived_event_unknown: i64,
    pub survival_30d_yes: i64,
    pub survival_30d_unknown: i64,
    pub fav_neurological_yes: i64,
    pub fav_neurological_unknown: i64,
}
