# LessPass command-line interface (CLI)

## Install

    python3 -m pip install --user lesspass

## Usage

    lesspass SITE [LOGIN] [MASTER_PASSWORD] [OPTIONS]

    Arguments:

    SITE                site used in the password generation (required)
    LOGIN               login used in the password generation
                        default to '' if not provided
    MASTER_PASSWORD     master password used in password generation
                        default to LESSPASS_MASTER_PASSWORD env variable or prompt

    Options:

    -l, --lowercase      add lowercase in password
    -u, --uppercase      add uppercase in password
    -d, --digits         add digits in password
    -s, --symbols        add symbols in password
    -L, --length         int (default 16, max 35)
    -C, --counter        int (default 1)
    -p, --prompt         interactively prompt SITE and LOGIN (prevent leak to shell history)
    --no-fingerprint     hide visual fingerprint of the master password when you type
    --no-lowercase       remove lowercase from password
    --no-uppercase       remove uppercase from password
    --no-digits          remove digits from password
    --no-symbols         remove symbols from password
    --exclude            remove chars from password
    -c, --clipboard      copy generated password to clipboard rather than displaying it.
                         Need pbcopy (OSX), xsel or xclip (Linux) or clip (Windows).
    -v, --version        lesspass version number

## Examples

### no symbols

    lesspass site login masterpassword --no-symbols

### no symbols shortcut

    lesspass site login masterpassword -lud

### only digits and length of 8

    lesspass site login masterpassword -d -L8

### master password in env variable

    LESSPASS_MASTER_PASSWORD="masterpassword" lesspass site login

## License

This project is licensed under the terms of the GNU GPLv3.
