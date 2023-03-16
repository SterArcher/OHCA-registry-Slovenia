use serde::Serialize;
use sqlx::MySqlPool;

#[derive(Debug, Serialize)]
pub struct BystanderResponse {
    pub bystander_cpr: BystanderCPR,
    pub bystander_aed: BystanderAED,
}

impl BystanderResponse {
    pub async fn new(pool: &MySqlPool) -> Self {
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
    pub async fn new(pool: &MySqlPool) -> Self {
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
