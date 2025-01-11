# vocpub-genericode

A small Python library supporting a Command Line Interface the converts RDF files conforming to the [VocPub Profile of SKOS](https://w3id.org/profile/vocpub) to Genericode and back.

## Use

### Command Line Interface

```
Usage: vpg [OPTIONS] COMMAND [ARGS]...                                             
                                                                                    
 Main callback for the CLI app                                                      
                                                                                    
╭─ Options ────────────────────────────────────────────────────────────────────────╮
│ --version             -v                                                         │
│ --help                -h        Show this message and exit.                      │
╰──────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────╮
│ r   Convert a Genericode file to VocPub SKOS RDF                                 │
│ g   Convert a ocPub SKOS RDF to Genericode                                       │
╰──────────────────────────────────────────────────────────────────────────────────╯
```

For each of the `r` and `g` commands:

```
╭─ Arguments ──────────────────────────────────────────────────────────────────────╮
│ *    file      PATH  [default: None] [required]                                  │
╰──────────────────────────────────────────────────────────────────────────────────╯
```

So you run it like this:

```
vpg r {FILE}
```

...and you get the Genericode file converted to SKOS RDF.