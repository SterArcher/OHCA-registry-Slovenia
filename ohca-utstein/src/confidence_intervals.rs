use statrs;
 


//1. Find the sample mean
//2. Calculate the standard deviation
//3. Find the standard error
//4. Find the margin of error
//5. Use these results in the formula

fn Calculate_confidence_interval(
    mean: f64,
    confidence: f64,
    standard_deviation: f64,
    sample_size: f64,
    z_value: f64,
   
) -> f64 {
    let sample_size;
    let standard_deviation;
    let standard_error: f64;
    let margin_error: f64;
    let confidence: f64; // in decimals ( for 90% use 0.9 for example)
    let confidence_interval;
    let mean;
    let values = vec![0; sample_size];
    let sum: f64;
    let z_value: f64;
    let sample_size:usize;


    let z;
    if confidence == 0.85 {
        z = 1.44;
    } else if confidence == 0.9 {
        z = 1.65;
    } else if confidence == 0.95 {
        z = 1.96;
    } else {
        print!("This is a WIP, for now we only have z values for the following confidence intervals -> 85% 90% 95%");
    }

  let i = 0;
    let sum = 0;
    loop {
        i += 1;
        sum += values[i];

        if i == sample_size {
            break;
        }
    }
    mean = sum / sample_size;


    loop {
        i += 1;
        sum = (values[i] - mean) * (values[i] - mean) + sum;

        if i == sample_size {
            break;
        }
    }
    standard_deviation = sum / sample_size;

  1.0 / (sample_size as f64).sqrt();

    if sample_size < 30 {
        confidence_interval = (mean as f64) + (confidence as f64) + ((standard_deviation as f64) / (sample_size as f64).sqrt());
    } else {        confidence_interval = (z as f64) * (standard_deviation as f64) + ((z as f64) * ((standard_deviation as f64) / (sample_size as f64).sqrt()));                                        
             };

             return confidence_interval;
        
}



