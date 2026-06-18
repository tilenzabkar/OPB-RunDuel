% rebase("base.tpl", user=user, success=success, error=error)

<h2>Prijava</h2>

<form method="post">
    <div class="mb-3">
        <label class="form-label">Uporabniško ime</label>
        <input class="form-control" name="uporabnisko_ime" required>
    </div>

    <div class="mb-3">
        <label class="form-label">Geslo</label>
        <input class="form-control" type="password" name="geslo" required>
    </div>

    <button class="btn btn-primary">Prijava</button>
</form>