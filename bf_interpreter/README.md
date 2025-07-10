# Brainfuck Interpreter

## Usage

```bash
cargo run <brainfuck_file>
```

## Example

```bash
$ cargo run helloworld.bf
Hello World!
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