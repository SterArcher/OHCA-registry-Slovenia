use serde::Serialize;
use sqlx::MySqlPool;

#[derive(Debug, Serialize)]
pub struct PatientOutcomes {
    pub all_ems_treated_arrests: Columns,
    pub ems_witnessed_excluded: EmsWitnessedExcluded,
}

impl PatientOutcomes {
    pub async fn new(pool: &MySqlPool) -> Self {
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
    pub async fn new(pool: &MySqlPool) -> Self {
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
