use serde::Serialize;
use sqlx::MySqlPool;

#[derive(Debug, Serialize)]
pub struct PatientOutcomes {
    pub ems_witnessed_included: EmsWitnessedIncluded,
    pub ems_witnessed_excluded: EmsWitnessedExcluded,
}

impl PatientOutcomes {
    pub async fn new(pool: &MySqlPool) -> Self {
        Self {
            ems_witnessed_included: EmsWitnessedIncluded::new(pool).await,
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
                WITH w AS 
                (
                    SELECT
                        rosc,
                        hospArri,
                        survival30d,
                        cpcDischarge,
                        mrsDischarge
                    FROM cases
                    WHERE witnesses = 1
                    AND bystanderAED = 1
                )
                SELECT
                    (SELECT COUNT(*) FROM w WHERE rosc = 1) AS "any_rosc_yes!: i64",
                    (SELECT COUNT(*) FROM w WHERE rosc = -1 OR rosc IS NULL) AS "any_rosc_unknown!: i64",
                    (SELECT COUNT(*) FROM w WHERE hospArri = 1) AS "survived_event_yes!: i64",
                    (SELECT COUNT(*) FROM w WHERE hospArri = -1 OR hospArri IS NULL) AS "survived_event_unknown!: i64",
                    (SELECT COUNT(*) FROM w WHERE survival30d = 1) AS "survival_30d_yes!: i64",
                    (SELECT COUNT(*) FROM w WHERE survival30d = -1 OR survival30d IS NULL) AS "survival_30d_unknown!: i64",
                    (SELECT COUNT(*) FROM w WHERE cpcDischarge = 2 OR mrsDischarge < 3) AS "fav_neurological_yes!: i64",
                    (SELECT COUNT(*) FROM w 
                        WHERE mrsDischarge = -2 OR mrsDischarge IS NULL OR cpcDischarge = -1 OR cpcDischarge IS NULL
                    ) AS "fav_neurological_unknown!: i64"
            "#
        ).fetch_one(pool)
        .await
        .unwrap();

        let shockable_bystander_cpr = sqlx::query_as!(
            Columns,
            r#"
                WITH w AS 
                (
                    SELECT
                        rosc,
                        hospArri,
                        survival30d,
                        cpcDischarge,
                        mrsDischarge
                    FROM cases
                    WHERE iniRythm = 0
                    AND reawitnesses != 2
                )
                SELECT
                    (SELECT COUNT(*) FROM cases WHERE witnesses = 1 AND bystanderAED = 1 AND rosc = 1) AS "any_rosc_yes!: i64",
                    (SELECT COUNT(*) FROM w WHERE rosc = -1 OR rosc IS NULL) AS "any_rosc_unknown!: i64",
                    (SELECT COUNT(*) FROM w WHERE hospArri = 1) AS "survived_event_yes!: i64",
                    (SELECT COUNT(*) FROM w WHERE hospArri = -1 OR hospArri IS NULL) AS "survived_event_unknown!: i64",
                    (SELECT COUNT(*) FROM w WHERE survival30d = 1) AS "survival_30d_yes!: i64",
                    (SELECT COUNT(*) FROM w WHERE survival30d = -1 OR survival30d IS NULL) AS "survival_30d_unknown!: i64",
                    (SELECT COUNT(*) FROM w WHERE cpcDischarge = 2 OR mrsDischarge < 3) AS "fav_neurological_yes!: i64",
                    (SELECT COUNT(*) FROM w 
                        WHERE mrsDischarge = -3 OR mrsDischarge IS NULL OR cpcDischarge = -1 OR cpcDischarge IS NULL
                    ) AS "fav_neurological_unknown!: i64"
            "#
        ).fetch_one(pool)
        .await
        .unwrap();

        let non_shockable_witnessed = sqlx::query_as!(
            Columns,
            r#"
                WITH w AS 
                (
                    SELECT
                        rosc,
                        hospArri,
                        survival30d,
                        cpcDischarge,
                        mrsDischarge
                    FROM cases
                    WHERE reawitnesses = 1
                )
                SELECT
                    (SELECT COUNT(*) FROM w WHERE rosc = 1) AS "any_rosc_yes!: i64",
                    (SELECT COUNT(*) FROM w WHERE rosc = -1 OR rosc IS NULL) AS "any_rosc_unknown!: i64",
                    (SELECT COUNT(*) FROM w WHERE hospArri = 1) AS "survived_event_yes!: i64",
                    (SELECT COUNT(*) FROM w WHERE hospArri = -1 OR hospArri IS NULL) AS "survived_event_unknown!: i64",
                    (SELECT COUNT(*) FROM w WHERE survival30d = 1) AS "survival_30d_yes!: i64",
                    (SELECT COUNT(*) FROM w WHERE survival30d = -1 OR survival30d IS NULL) AS "survival_30d_unknown!: i64",
                    (SELECT COUNT(*) FROM w WHERE cpcDischarge = 2 OR mrsDischarge < 3) AS "fav_neurological_yes!: i64",
                    (SELECT COUNT(*) FROM w 
                        WHERE mrsDischarge = -4 OR mrsDischarge IS NULL OR cpcDischarge = -1 OR cpcDischarge IS NULL
                    ) AS "fav_neurological_unknown!: i64"
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
pub struct EmsWitnessedIncluded {
    pub all_ems_treated_arrests: Columns,
}

impl EmsWitnessedIncluded {
    pub async fn new(pool: &MySqlPool) -> Self {
        let all_ems_treated_arrests = sqlx::query_as!(
            Columns,
            r#"
                WITH w AS 
                (
                    SELECT
                        rosc,
                        hospArri,
                        survival30d,
                        cpcDischarge,
                        mrsDischarge
                    FROM cases
                    WHERE witnesses BETWEEN 1 AND 2
                )
                SELECT
                    (SELECT COUNT(*) FROM w WHERE rosc = 1) AS "any_rosc_yes!: i64",
                    (SELECT COUNT(*) FROM w WHERE rosc = -1 OR rosc IS NULL) AS "any_rosc_unknown!: i64",
                    (SELECT COUNT(*) FROM w WHERE hospArri = 1) AS "survived_event_yes!: i64",
                    (SELECT COUNT(*) FROM w WHERE hospArri = -1 OR hospArri IS NULL) AS "survived_event_unknown!: i64",
                    (SELECT COUNT(*) FROM w WHERE survival30d = 1) AS "survival_30d_yes!: i64",
                    (SELECT COUNT(*) FROM w WHERE survival30d = -1 OR survival30d IS NULL) AS "survival_30d_unknown!: i64",
                    (SELECT COUNT(*) FROM w WHERE cpcDischarge = 2 OR mrsDischarge < 3) AS "fav_neurological_yes!: i64",
                    (SELECT COUNT(*) FROM w 
                        WHERE mrsDischarge = -1 OR mrsDischarge IS NULL OR cpcDischarge = -1 OR cpcDischarge IS NULL
                    ) AS "fav_neurological_unknown!: i64"
                "#
        )
        .fetch_one(pool)
        .await
        .unwrap();

        Self {
            all_ems_treated_arrests,
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
