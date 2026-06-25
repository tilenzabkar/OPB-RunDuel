% rebase("base.tpl", user=user, success=success, error=error)

<div class="page-header mb-4">
    <div>
        <p class="dashboard-eyebrow mb-1">Nova aktivnost</p>
        <h2 class="page-title mb-1">Dodaj tek</h2>
        <p class="text-muted-soft mb-0">
            Ročno vnesi datum, razdaljo in trajanje teka.
        </p>
    </div>

    <a class="btn btn-secondary" href="{{url('runs')}}">
        <i class="bi bi-arrow-left me-1"></i>
        Nazaj na teke
    </a>
</div>

<div class="row justify-content-center">
    <div class="col-lg-7">
        <div class="card form-card run-form-card">
            <form method="post">
                <div class="form-section-title">
                    <i class="bi bi-calendar-event"></i>
                    Podatki o teku
                </div>

                <div class="mb-3">
                    <label class="form-label">Datum</label>
                    <input class="form-control form-control-lg" type="datetime-local" name="datum">
                    <small class="form-text text-muted">
                        Če pustiš prazno, aplikacija uporabi trenutni čas.
                    </small>
                </div>

                <div class="mb-3">
                    <label class="form-label">Razdalja</label>
                    <div class="input-group input-group-lg">
                        <input class="form-control" type="number" step="0.01" min="0.01" name="razdalja" required>
                        <span class="input-group-text">km</span>
                    </div>
                </div>

                <div class="mb-4">
                    <label class="form-label">Trajanje</label>
                    <div class="duration-grid">
                        <div class="duration-field">
                            <input type="number" name="ure" class="form-control form-control-lg" min="0" value="0">
                            <span>ur</span>
                        </div>

                        <div class="duration-field">
                            <input type="number" name="minute" class="form-control form-control-lg" min="0" max="59" value="0">
                            <span>min</span>
                        </div>

                        <div class="duration-field">
                            <input type="number" name="sekunde" class="form-control form-control-lg" min="0" max="59" value="0">
                            <span>s</span>
                        </div>
                    </div>
                </div>

                <div class="d-flex flex-wrap gap-2">
                    <button class="btn btn-success btn-lg" type="submit">
                        <i class="bi bi-check-lg me-1"></i>
                        Shrani tek
                    </button>

                    <a class="btn btn-secondary btn-lg" href="{{url('runs')}}">
                        Prekliči
                    </a>
                </div>
            </form>
        </div>
    </div>
</div>