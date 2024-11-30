import chroma
import shell
import switchboard
import answers

bench = {
    "Database": chroma.invoke,
    "Shell": shell.invoke,
    "Switchboard": switchboard.invoke,
    "Answers": answers.invoke,
}
