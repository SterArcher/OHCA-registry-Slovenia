use bigdecimal::ToPrimitive;
use chrono::NaiveTime;
use serde::Serialize;
use sqlx::MySqlPool;
use statrs::distribution::{Continuous, Normal};

#[derive(Debug, Serialize)]
pub struct Utstein {
    system_core: Core,
    dispatcher_id_ca: DispatcherIdCA,
    dispatcher_cpr: DispatcherCPR,
    resc_attempted: RescAttempted,
    resc_not_attempted: RescNotAttempted,
    location: Location,
    patient: Patient,
    witnessed: Witnessed,
    bystander_response: BystanderResponse,
    etiology: Etiology,
    ems_process: EMSProcess,
    hospital_process: HospitalProcess,
    patient_outcomes: PatientOutcomes,
}

impl Utstein {
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

#[derive(Debug, Serialize)]
struct Core {
    population_served: i64,
    cardiac_arrests_attended: i64,
    response_time_mean: f64,
    response_time_std: f64,
    response_time: String,
}

impl Core {
    async fn new(pool: &MySqlPool) -> Self {
        let record = sqlx::query!(
            r#"
                SELECT 
                    (SELECT SUM(population) AS "population_served!: i64" FROM systems) AS population_served,
                    (SELECT SUM(attendedCAs) FROM systems) AS cardiac_arrests_attended,
                    (SELECT AVG(responseTime) FROM cases WHERE responseTime IS NOT NULL) AS response_time_mean,
                    (SELECT STD(responseTime) FROM cases WHERE responseTime IS NOT NULL) AS response_time_std,
                    (SELECT NULL) as "response_time: String"
            "#
        )
        .fetch_one(pool)
        .await
        .unwrap();

        let mut core = Core {
            population_served: record.population_served.unwrap().to_i64().unwrap(),
            cardiac_arrests_attended: record.cardiac_arrests_attended.unwrap().to_i64().unwrap(),
            response_time_mean: record.response_time_mean.unwrap().to_f64().unwrap(),
            response_time_std: record.response_time_std.unwrap(),
            response_time: String::new(),
        };

        let distribution = Normal::new(core.response_time_mean, core.response_time_std).unwrap();
        let pdf = distribution.pdf(90.);
        let duration = NaiveTime::from_num_seconds_from_midnight_opt(pdf as u32, 0).unwrap();

        core.response_time = duration.to_string();

        core
    }
}

#[derive(Debug, Serialize)]
struct DispatcherIdCA {
    yes: i64,
    no: i64,
    unknown: i64,
}

impl DispatcherIdCA {
    async fn new(pool: &MySqlPool) -> Self {
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

#[derive(Debug, Serialize)]
struct DispatcherCPR {
    yes: i64,
    no: i64,
    unknown: i64,
}

impl DispatcherCPR {
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

#[derive(Debug, Serialize)]
struct RescAttempted {
    vf: i64,
    vt: i64,
    pea: i64,
    asys: i64,
    brady: i64,
    aed_non_shockable: i64,
    aed_shockable: i64,
    not_recorded: i64,
    unknown: i64,
}

impl RescAttempted {
    async fn new(pool: &MySqlPool) -> Self {
        // Query with a common table expression - CTE
        // Read more at https://mariadb.com/kb/en/with/
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

#[derive(Debug, Serialize)]
struct RescNotAttempted {
    all_cases: i64,
    dnar: i64,
    obviously_dead: i64,
    signs_of_life: i64,
}

impl RescNotAttempted {
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
struct Location {
    home: i64,
    work: i64,
    rec: i64,
    public: i64,
    educ: i64,
    nursing: i64,
    other: i64,
    unknown: i64,
}

impl Location {
    async fn new(pool: &MySqlPool) -> Self {
        sqlx::query_as!(
            Location,
            r#"
                SELECT
                    (SELECT COUNT(*) FROM cases WHERE location = 1) AS "home!: i64",
                    (SELECT COUNT(*) FROM cases WHERE location = 2) AS "work!: i64",
                    (SELECT COUNT(*) FROM cases WHERE location = 3) AS "rec!: i64",
                    (SELECT COUNT(*) FROM cases WHERE location = 5) AS "public!: i64",
                    (SELECT COUNT(*) FROM cases WHERE location = 7) AS "educ!: i64",
                    (SELECT COUNT(*) FROM cases WHERE location = 6) AS "nursing!: i64",
                    (SELECT COUNT(*) FROM cases WHERE location = 8) AS "other!: i64",
                    (SELECT COUNT(*) FROM cases WHERE location = -1 OR location IS NULL) AS "unknown!: i64"
            "#
        )
        .fetch_one(pool)
        .await
        .unwrap()
    }
}

#[derive(Debug, Serialize)]
struct Patient {
    age: Age,
    sex: Sex,
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
struct Age {
    mean: f64,
    unknown: i64,
}

impl Age {
    async fn new(pool: &MySqlPool) -> Self {
        let record = sqlx::query!(
            r#"
                SELECT
                    AVG(age) AS mean,
                    (SELECT COUNT(*) FROM cases WHERE age IS NULL) AS "unknown!: i64"
                FROM cases
            "#
        )
        .fetch_one(pool)
        .await
        .unwrap();

        Self {
            mean: record.mean.unwrap().to_f64().unwrap(),
            unknown: record.unknown,
        }
    }
}

#[derive(Debug, Serialize)]
struct Sex {
    male: i64,
    female: i64,
    unknown: i64,
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
struct Witnessed {
    bystander: i64,
    ems: i64,
    unwitnessed: i64,
    unknown: i64,
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
struct BystanderResponse {
    bystander_cpr: BystanderCPR,
    bystander_aed: BystanderAED,
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
struct BystanderCPR {
    no_bcpr: i64,
    bcpr: i64,
    cc_only: i64,
    cc_or_vent: i64,
    unknown: i64,
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
struct BystanderAED {
    analyse: i64,
    shock: i64,
    unknown: i64,
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
struct Etiology {
    medical: i64,
    trauma: i64,
    overdose: i64,
    drowning: i64,
    electrocution: i64,
    asphyxial: i64,
    not_recorded: i64,
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
struct EMSProcess {
    first_defib_time: f64,

    // targeted temp control
    indicated_done: i64,
    indicated_not_done: i64,
    not_indicated: i64,
    unknown: i64,

    // drugs given
    drugs_given: i64,
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
struct HospitalProcess {
    // reperfusion
    attempted: i64,

    // targeted temp control
    indicated_done: i64,
    indicated_not_done: i64,
    not_indicated: i64,
    unknown: i64,

    // organ donation
    organ_donation: i64,
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
struct PatientOutcomes {
    all_ems_treated_arrests: Columns,
    ems_witnessed_excluded: EmsWitnessedExcluded,
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
struct EmsWitnessedExcluded {
    shockable_bystander_witnessed: Columns,
    shockable_bystander_cpr: Columns,
    non_shockable_witnessed: Columns,
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
struct Columns {
    any_rosc_yes: i64,
    any_rosc_unknown: i64,
    survived_event_yes: i64,
    survived_event_unknown: i64,
    survival_30d_yes: i64,
    survival_30d_unknown: i64,
    fav_neurological_yes: i64,
    fav_neurological_unknown: i64,
}
