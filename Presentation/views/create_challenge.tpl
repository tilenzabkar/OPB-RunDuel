% rebase("base.tpl", user=user, success=success, error=error)

<h2>Nov izziv</h2>

<form method="post">
    <div class="mb-3">
        <label class="form-label">Vrsta izziva</label>
        <select class="form-select" name="vrsta" required>
            % for tip in tipi:
                <option value="{{tip.value}}">{{tip.value}}</option>
            % end
        </select>
    </div>

    <div class="mb-3">
        <label class="form-label">Nasprotnik</label>
        <select class="form-select" name="nasprotnik_id" required>
            % for u in uporabniki:
                <option value="{{u.id}}">
                    {{u.uporabnisko_ime}} - {{u.stanje}} kovancev
                </option>
            % end
        </select>
    </div>

    <div class="mb-3">
        <label class="form-label">Tvoje stanje</label>
        <div class="alert alert-info d-flex align-items-center" role="alert">
            <i class="bi bi-coin me-2"></i>
            {{ user['stanje'] }} kovancev na voljo.
        </div>
    </div>

    <div class="mb-3">
        <label class="form-label">Stava</label>
        <input class="form-control" type="number" name="stava" 
               min="1" max="{{ user['stanje'] }}" required>
        <small class="form-text text-muted">
            Vpišite znesek med 1 in {{ user['stanje'] }} kovancev.
        </small>
    </div>

    <button class="btn btn-success">Ustvari</button>
    <a class="btn btn-secondary" href="/challenges">Nazaj</a>
</form>