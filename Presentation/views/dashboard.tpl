% rebase("base.tpl", user=user, success=success, error=error)

<div class="dashboard-header mb-4">
    <div>
        <p class="dashboard-eyebrow mb-1">Pozdravljen nazaj</p>
        <h2 class="page-title mb-1">Dashboard</h2>
        <p class="text-muted-soft mb-0">
            Prijavljen si kot <strong>{{user["uporabnisko_ime"]}}</strong>
        </p>
    </div>

    <div class="coins-pill">
        <i class="bi bi-coin"></i>
        <span>{{user["stanje"]}} kovancev</span>
    </div>
</div>

<div class="row g-4 mb-4">
    <div class="col-md-4">
        <div class="card stat-card">
            <div class="stat-icon">
                <i class="bi bi-person-walking"></i>
            </div>
            <div>
                <div class="stat-number">{{len(teki)}}</div>
                <div class="stat-label">Število tekov</div>
            </div>
        </div>
    </div>

    <div class="col-md-4">
        <div class="card stat-card">
            <div class="stat-icon">
                <i class="bi bi-map"></i>
            </div>
            <div>
                <div class="stat-number">{{round(skupna_razdalja, 2)}} km</div>
                <div class="stat-label">Skupna razdalja</div>
            </div>
        </div>
    </div>

    <div class="col-md-4">
        <div class="card stat-card">
            <div class="stat-icon">
                <i class="bi bi-stopwatch"></i>
            </div>
            <div>
                <div class="stat-number">{{format_trajanje(skupno_trajanje)}}</div>
                <div class="stat-label">Skupni čas</div>
            </div>
        </div>
    </div>
</div>

<div class="row g-4">
    <div class="col-lg-7">
        <div class="card dashboard-card">
            <div class="d-flex justify-content-between align-items-start mb-3">
                <div>
                    <h4 class="mb-1">Teki</h4>
                    <p class="text-muted-soft mb-0">Dodajaj aktivnosti in spremljaj svojo statistiko.</p>
                </div>
                <span class="dashboard-badge">Število tekov: {{len(teki)}}</span>
            </div>

            <div class="dashboard-actions">
                <a class="btn btn-primary" href="{{url('runs')}}">
                    <i class="bi bi-list-ul me-1"></i>
                    Poglej teke
                </a>
                <a class="btn btn-success" href="{{url('runs/new')}}">
                    <i class="bi bi-plus-lg me-1"></i>
                    Dodaj tek
                </a>
                <a class="btn btn-warning" href="{{url('strava/connect')}}">
                    <i class="bi bi-cloud-arrow-down me-1"></i>
                    Uvozi iz Strave
                </a>
                <a class="btn btn-danger" href="{{url('strava/logout')}}" target="_blank" rel="noopener noreferrer">
                    <i class="bi bi-box-arrow-right me-1"></i>
                    Odjava iz Strave
                </a>
                % if not STRAVA_CLIENT_ID:
                    <form action="{{url('strava/setup')}}" method="post" class="mt-3 w-100">
                        <input class="form-control mb-2" name="client_id" placeholder="Strava Client ID" required>
                        <input class="form-control mb-2" name="client_secret" placeholder="Strava Client Secret" required>
                        <button class="btn btn-outline-primary w-100" type="submit">
                            Shrani Strava podatke
                        </button>
                    </form>
                % end
            </div>
        </div>
    </div>

    <div class="col-lg-5">
        <div class="card dashboard-card">
            <div class="d-flex justify-content-between align-items-start mb-3">
                <div>
                    <h4 class="mb-1">Izzivi</h4>
                    <p class="text-muted-soft mb-0">Tekmuj s prijatelji in zbiraj kovance.</p>
                </div>
                <span class="dashboard-badge">Število izzivov: {{len(izzivi)}}</span>
            </div>

            <div class="dashboard-actions">
                <a class="btn btn-primary" href="{{url('challenges')}}">
                    <i class="bi bi-trophy me-1"></i>
                    Poglej izzive
                </a>
                <a class="btn btn-success" href="{{url('challenges/new')}}">
                    <i class="bi bi-plus-lg me-1"></i>
                    Nov izziv
                </a>
            </div>
        </div>
    </div>
</div>