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
        <div class="input-group">
            <input type="number" name="ure" class="form-control" min="0" value="0">
            <span class="input-group-text">h</span>
            <input type="number" name="minute" class="form-control" min="0" max="59" value="0">
            <span class="input-group-text">min</span>
            <input type="number" name="sekunde" class="form-control" min="0" max="59" value="0">
            <span class="input-group-text">s</span>
        </div>
    </div>

    <button class="btn btn-success">Shrani</button>
    <a class="btn btn-secondary" href="/runs">Nazaj</a>
</form>