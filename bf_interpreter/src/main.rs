use std::{fs::{self}, io::{stdin, stdout, Read, Write}, path::PathBuf};

use clap::Parser;

#[derive(Parser, Debug)]
#[command(version)]
struct Args {

    #[arg()]
    file: PathBuf,
}

fn main() {
    let args = Args::parse();

    
    let mut mem = [0u8; 30_000];
    let mut d_ptr = 0;
    let mut i_ptr = 0;
    let debug = false;

    let prog = fs::read(args.file).unwrap();

    loop {
        if i_ptr >= prog.len() {
            break;
        }

        match prog[i_ptr] {
            b'$' => {
                if debug {
                    for b in &mem[..10] {
                        print!("{} ",b);
                    }
                    println!();
                }
                i_ptr += 1;
            },
            b'>' => {
                d_ptr += 1; 
                i_ptr += 1;
            },
            b'<' => { 
                d_ptr -= 1; 
                i_ptr += 1;
            },
            b'+' => { 
                mem[d_ptr] += 1; 
                i_ptr += 1;
            },
            b'-' => { 
                mem[d_ptr] -= 1; 
                i_ptr += 1;
            },
            b'.' => { 
                print!("{}", mem[d_ptr] as char); stdout().flush().unwrap(); 
                i_ptr += 1;
            },
            b',' => {
                stdin().read_exact(&mut mem[d_ptr..d_ptr + 1]).unwrap();
                i_ptr += 1;
            }
            b'[' => {
                if mem[d_ptr] != 0 {
                    i_ptr += 1;
                    continue;
                }

                let original_position = i_ptr;
                let mut stack = 1;
                loop {
                    i_ptr += 1;
                    if i_ptr >= prog.len() {
                        panic!("Unable to find matching ']' for '[' at position {}", original_position);
                    }

                    match prog[i_ptr] {
                        b'[' => { stack += 1; },
                        b']' => { stack -= 1; },
                        _ => (),
                    }

                    if stack == 0 {
                        break;
                    }
                }
            },
            b']' => {
                if mem[d_ptr] == 0 {
                    i_ptr += 1;
                    continue;
                }

                let original_position = i_ptr;
                let mut stack = 1;
                loop {
                    if i_ptr == 0 {
                        panic!("Unable to find matching '[' for ']' at position {}", original_position);
                    }

                    i_ptr -= 1;

                    match prog[i_ptr] {
                        b']' => { stack += 1; },
                        b'[' => { stack -= 1; },
                        _ => (),
                    }

                    if stack == 0 {
                        break;
                    }
                }
            },
            _ => {
                i_ptr += 1;
            }
        }
    }
}
