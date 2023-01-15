//1. Find the sample mean
//2. Calculate the standard deviation
//3. Find the standard error
//4. Find the margin of error
//5. Use these results in the formula

/// Confidence in decimals ( for 90% use 0.9 for example)
fn calculate_confidence_interval(values_total: Vec<i64> ,values_sample: Vec<i64>, confidence: f64) -> () {
    let confidence_interval_upper: f64;
    let confidence_interval_lower: f64;

    let value_sample_length = values_sample.len();
    let value_total_length = values_total.len();

    // TODO: fix this
    let _z = match confidence {
        0.7  => 1.036,
        0.75 => 1.150,
        0.8  => 1.282,
        0.85 => 1.44,
        0.9  => 1.65,
        0.95 => 1.96,
        0.98 => 2.326,
        0.99 => 2.576,
           _ => panic!(),
    };

    let sum_sample: i64 = values_sample.iter().sum();
    let mut sum_s = sum_sample as f64;

    let sum_population: i64 = values_total.iter().sum();
    let sum_p = sum_population as f64;

    let mean = sum_s / value_sample_length as f64;
    let population_mean = sum_p / value_total_length as f64;

    for i in 0..value_sample_length {
        let diff: f64 = values_sample[i] as f64 - mean;
        sum_s = diff.powi(2) + sum_s as f64;
    }

    let standard_deviation = sum_s / value_sample_length as f64;
    let t_value = (mean - population_mean)/(standard_deviation / (value_sample_length as f64).sqrt());
    // 1.0 / (value_length as f64).sqrt();   what is this formula?

    if value_sample_length < 29 {
        confidence_interval_upper = (mean as f64 ) + (t_value as f64) * (((standard_deviation as f64) / (value_sample_length as f64).sqrt()));
        confidence_interval_lower = (mean as f64 ) - (t_value as f64) * (((standard_deviation as f64) / (value_sample_length as f64).sqrt()));
    } else {
        confidence_interval_upper = (mean as f64 ) + (confidence as f64) * (((standard_deviation as f64) / (value_sample_length as f64).sqrt()));
        confidence_interval_lower = (mean as f64 ) - (confidence as f64) * (((standard_deviation as f64)/ (value_sample_length  as f64).sqrt()));
    };

    (confidence_interval_lower , confidence_interval_upper);
}

/* 
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
*/