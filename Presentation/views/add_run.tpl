% rebase("base.tpl", user=user, success=success, error=error)

<h2>Dodaj tek</h2>

<form method="post">
    <div class="mb-3">
        <label class="form-label">Datum</label>
        <input class="form-control" type="datetime-local" name="datum">
    </div>

    <div class="mb-3">
        <label class="form-label">Razdalja</label>
        <input class="form-control" type="number" step="0.01" name="razdalja" required>
    </div>

    <div class="mb-3">
        <label class="form-label">Trajanje</label>
        <input class="form-control" type="number" name="trajanje" required>
        <div class="form-text">
            Vnesi trajanje v minutah. Primer: 90 pomeni 1 h 30 min.
        </div>
    </div>

    <button class="btn btn-success">Shrani</button>
    <a class="btn btn-secondary" href="/runs">Nazaj</a>
</form>