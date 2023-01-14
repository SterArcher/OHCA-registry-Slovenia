use statrs;

//1. Find the sample mean
//2. Calculate the standard deviation
//3. Find the standard error
//4. Find the margin of error
//5. Use these results in the formula

/// Confidence in decimals ( for 90% use 0.9 for example)
fn calculate_confidence_interval(values: Vec<i64>, confidence: f64) -> f64 {
    let confidence_interval;

    let value_length = values.len();

    // TODO: fix this
    let z = match confidence {
        0.85 => 1.44,
        0.9 => 1.65,
        0.95 => 1.96,
        _ => panic!(),
    };

    let sum: i64 = values.iter().sum();
    let mut sum_f = sum as f64;

    let mean = sum_f / value_length as f64;

    for i in 0..value_length {
        let diff: f64 = values[i] as f64 - mean;
        sum_f = diff.powi(2) + sum_f as f64;
    }

    let standard_deviation = sum_f / value_length as f64;

    // 1.0 / (value_length as f64).sqrt();

    if value_length < 30 {
        confidence_interval = (mean as f64)
            + (confidence as f64)
            + ((standard_deviation as f64) / (value_length as f64).sqrt());
    } else {
        confidence_interval = (z as f64) * (standard_deviation as f64)
            + ((z as f64) * ((standard_deviation as f64) / (value_length as f64).sqrt()));
    };

    return confidence_interval;
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_confidence_interval() {
        let values = vec![10, 20, 30, 50, 20];
        let confidence_interval = calculate_confidence_interval(values, 0.9);

        assert_eq!(confidence_interval, 120.81485505499117);

        let values = vec![10, 30, 30, 50, 20];
        assert_eq!(
            calculate_confidence_interval(values, 0.9),
            120.13157348199141
        );
    }
}
