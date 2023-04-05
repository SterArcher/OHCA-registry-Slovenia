pub fn confidence_interval_90(count: i64, mean: f64, std: f64) -> (f64, f64) {
    let interval = (1.645 * std) / (count as f64).sqrt();
    (mean, interval)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_confidence_interval_90() {
        assert_eq!(
            confidence_interval_90(12, 4.916666666666666, 2.5030284687057627),
            (4.916666666666666, 1.188614621761678)
        )
    }
}
