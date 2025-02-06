fn main() {
    let bit_value: i64 = 000272362142333;
    // Decode bit value of flight software version
    let major = (bit_value >> 24) & 0xFF;
    let minor = (bit_value >> 16) & 0xFF;
    let patch = (bit_value >> 8) & 0xFF;
    println!("{},{},{}", major, minor, patch);
}
