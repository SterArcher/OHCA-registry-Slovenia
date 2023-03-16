use serde::Serialize;
use sqlx::MySqlPool;

use self::core::*;
use bystander_response::*;
use dispatcher_cpr::*;
use dispatcher_id_ca::*;
use ems_process::*;
use etiology::*;
use hospital_process::*;
use location::*;
use patient::*;
use patient_outcomes::*;
use resc_attempted::*;
use resc_not_attempted::*;
use witnessed::*;

pub mod bystander_response;
pub mod core;
pub mod dispatcher_cpr;
pub mod dispatcher_id_ca;
pub mod ems_process;
pub mod etiology;
pub mod hospital_process;
pub mod location;
pub mod patient;
pub mod patient_outcomes;
pub mod resc_attempted;
pub mod resc_not_attempted;
pub mod witnessed;

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
