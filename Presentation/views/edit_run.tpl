% rebase("base.tpl", user=user, success=success, error=error)

<h2>Uredi tek</h2>

<form method="post" action="/runs/{{ tek.id }}/edit">
    <div class="mb-3">
        <label class="form-label">Datum</label>
        <input class="form-control" type="datetime-local" name="datum" 
               value="{{ tek.datum.strftime('%Y-%m-%dT%H:%M') }}" required>
    </div>

    <div class="mb-3">
        <label class="form-label">Razdalja</label>
        <input class="form-control" type="number" step="0.01" name="razdalja" 
               value="{{ tek.razdalja }}" required>
    </div>

    <div class="mb-3">
        <label class="form-label">Trajanje</label>
        <div class="input-group">
            % hours = tek.trajanje // 3600
            % minutes = (tek.trajanje % 3600) // 60
            % seconds = tek.trajanje % 60
            <input type="number" name="ure" class="form-control" min="0" value="{{ hours }}">
            <span class="input-group-text">h</span>
            <input type="number" name="minute" class="form-control" min="0" max="59" value="{{ minutes }}">
            <span class="input-group-text">min</span>
            <input type="number" name="sekunde" class="form-control" min="0" max="59" value="{{ seconds }}">
            <span class="input-group-text">s</span>
        </div>
    </div>

    <button class="btn btn-primary" type="submit">Shrani spremembe</button>
    <a class="btn btn-secondary" href="/runs">Prekliči</a>
</form>