use std::io;
use std::num::Float;

fn main() {
let sample_size
let standard_deviation
let standard_error
let margin_error
let confidence
let confidence_interval
let mean
let values = vec![0; sample_size];
let sum

}

fn Calculate_mean(sample_size: i32, values: [f32; sample_size]) -> f32 
{
    let i = 0
    let sum = 0
    loop {
        i += 1;
        sum += values[i]

        if i == sample_size {
            break;
            }   
        }
    mean = sum /sample_size
 
}

fn Calculate_standard_deviation(sample_size: i32, values: [f32; sample_size], mean:f32)  -> f32  
{
    let i = 0
    let sum = 0
    loop {
        i += 1;
        sum =  (values[i] - mean) * (values[i] - mean) + sum 

        if i == sample_size {
            break;
            }   
        }
        standard_deviation = sum / sample_size
}

fn Calculate_standard_error(sample_size: i32, standard_deviation: f32)   -> f32
{
  standard_error = standard_deviation / sample
}

fn Calculate_margin_error(sample_size) -> f32 {

    1 / sqrt(sample_size)

}

fn Calculate_confidence_interval(mean: f32, confidence: i32, standard_deviation: f32, sample_size:i32) ->f32   
{
  confidence_interval = mean + confidence (standard_deviation / sqrt(sample_size))
}