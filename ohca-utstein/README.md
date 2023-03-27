# Export script for the OHCA Registry Slovenia

To use, copy `.env.example` to `.env`  and specify the correct connection string.


# Developing

Tailwind is used to help with stying the `index.html` Utstein report template. To aid with that, the crate `railwind` is used. To start using it, run:

> cargo install railwind_cli

After installing it, navigate to this directory and run:

> railwind -w -p

To run `railwind_cli` and watch the `index.html` file for changes.