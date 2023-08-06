# git-sign-off

Add and check git signatures to your repository to check conditions/tasks automatically.

Do you like automation?! So do we!

Check any command success through `git sign-off` calls in your git pre-commit hooks. On your CI, check that they are up-to-date with a simple `git sign-off-check`.

This way you can even ensure your fellow developers have their hooks installed and running correctly.

# Installation

```bash
pip install git-sign-off
```

This installs programs `git-sign-off` and `git-sign-off-check`. Use them directly or through git commands.

# Usage


### Create certificate

Prove that a command ran successfully locally through:

```bash
git sign-off -c bash <run_my_local_sensitive_test.sh>
```

If the "challenge" command executes successfully a certificate is added to your commit. You will then see the message:
> Added git-sign-off signature for task 'default'.


### Check certificate

Useful in CI or for other developers:

```bash
git sign-off-check
```
If your certificate is up-to-date you will see:
> Signature check for task 'default' passed.

If your certificate is not up-to-date you will have an error like:
>SignatureError: Outdated signature found. Latest signature was generated after commit:
>5c1537d3502b8bc17172b5a03a4531b010024754



