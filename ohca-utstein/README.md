# Export script for the OHCA Registry Slovenia

To use the CLI, install it with `cargo install ohca-utstein` and run it using `ohca-utstein commands`.

To connect to a database using credentials and output a `utstein.json` file use:

> `ohca-utstein json credentails -u user -d database_name -i 127.0.0.1:3306`

You will be prompted for the database password.

To connect using a connection string and output a `utstein_report.html` file use:

> `ohca-utstein html -o utstein_report.html connect -c mysql://{user}:{password}@{host}:{port}/{db}`

# Developing

Tailwind is used to help with stying the `index.html` Utstein report template. To aid with that, the crate `railwind` is used. To start using it, run:

> cargo install railwind_cli

After installing it, navigate to this directory and run:

> railwind -w -p

To run `railwind_cli` and watch the `index.html` file for changes.