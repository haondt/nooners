# Brainfuck Interpreter

A simple Brainfuck interpreter written in Rust.

## Usage

```bash
cargo run <brainfuck_file>
```

## Example

Create a file `hello.bf` with the classic "Hello, World!" program:

```
++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.
```

Run it:

```bash
cargo run hello.bf
```

## Brainfuck Commands

- `>` - Move data pointer right
- `<` - Move data pointer left
- `+` - Increment the byte at data pointer
- `-` - Decrement the byte at data pointer
- `.` - Output the byte at data pointer
- `,` - Input a byte and store it at data pointer
- `[` - Jump forward if byte at data pointer is zero
- `]` - Jump backward if byte at data pointer is nonzero
- `$` - Debug: print first 10 memory cells

## Features

- 30,000 byte memory tape
- Standard Brainfuck command set
- Debug output option
- Command-line argument parsing with clap
