use std::io;
use std::num::Float;

//1. Find the sample mean
//2. Calculate the standard deviation
//3. Find the standard error
//4. Find the margin of error
//5. Use these results in the formula

fn Calculate_confidence_interval(
    mean: f32,
    confidence: i32,
    standard_deviation: f32,
    sample_size: i32,
    z_value: f32,
) -> f32 {
    let sample_size;
    let standard_deviation;
    let standard_error;
    let margin_error;
    let confidence; // in decimals ( for 90% use 0.9 for example)
    let confidence_interval;
    let mean;
    let values = vec![0; sample_size];
    let sum;
    let z_value;

    if sample_size < 30 {
        confidence_interval = mean + confidence(standard_deviation / sqrt(sample_size))
    } else {
        confidence_interval =
            z * standard_deviation + (z * (standard_deviation / sqrt(sample_size)))
    }
}

fn Calculate_mean(sample_size: i32, values: [f32; sample_size]) -> f32 {
    let i = 0;
    let sum = 0;
    loop {
        i += 1;
        sum += values[i];

        if i == sample_size {
            break;
        }
    }
    mean = sum / sample_size
}

fn Calculate_standard_deviation(sample_size: i32, values: [f32; sample_size], mean: f32) -> f32 {
    let i = 0;
    let sum = 0;
    loop {
        i += 1;
        sum = (values[i] - mean) * (values[i] - mean) + sum;

        if i == sample_size {
            break;
        }
    }
    standard_deviation = sum / sample_size
}

fn Calculate_margin_error(sample_size: i32) -> f32 {
    1 / sqrt(sample_size)
}

fn Calculate_z_value(confidence: f32) {
    if confidence = 0.85 {
        return z = 1.44;
    } else if confidence = 0.9 {
        return z = 1.65;
    } else if confidence = 0.95 {
        return z = 1.96;
    } else {
        print!("This is a WIP, for now we only have z values for the following confidence intervals -> 85% 90% 95%");
    }
}
