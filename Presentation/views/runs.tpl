% rebase("base.tpl", user=user, success=success, error=error)

<div class="page-header mb-4">
    <div>
        <p class="dashboard-eyebrow mb-1">Aktivnosti</p>
        <h2 class="page-title mb-1">Moji teki</h2>
        <p class="text-muted-soft mb-0">
            Pregled vseh ročno dodanih in uvoženih tekov.
        </p>
    </div>

    <a class="btn btn-primary" href="{{url('runs/new')}}">
        <i class="bi bi-plus-lg me-1"></i>
        Dodaj tek
    </a>
</div>

<div class="card runs-actions-card mb-4">
    <div class="d-flex flex-wrap gap-2 justify-content-between align-items-center">
        <div>
            <h5 class="mb-1">Strava uvoz</h5>
            <p class="text-muted-soft mb-0">
                Uvozi aktivnosti iz Strave ali se odjavi iz povezave.
            </p>
        </div>

        <div class="d-flex flex-wrap gap-2">
            <a class="btn btn-warning" href="{{url('strava/connect')}}">
                <i class="bi bi-cloud-arrow-down me-1"></i>
                Uvozi iz Strave
            </a>

            <a class="btn btn-danger" href="{{url('strava/logout')}}" target="_blank" rel="noopener noreferrer">
                <i class="bi bi-box-arrow-right me-1"></i>
                Odjava iz Strave
            </a>
        </div>
    </div>
</div>

<div class="card table-card">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h4 class="mb-0">Seznam tekov</h4>
        <span class="dashboard-badge">Število tekov: {{len(teki)}}</span>
    </div>

    % if len(teki) == 0:
        <div class="empty-state">
            <div class="empty-icon">
                <i class="bi bi-activity"></i>
            </div>
            <h5>Ni še dodanih tekov</h5>
            <p class="text-muted-soft mb-3">
                Dodaj prvi tek ali ga uvozi iz Strave.
            </p>
            <a class="btn btn-primary" href="{{url('runs/new')}}">
                Dodaj prvi tek
            </a>
        </div>
    % else:
        <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
                <thead>
                    <tr>
                        <th>Datum</th>
                        <th>Razdalja</th>
                        <th>Trajanje</th>
                        <th class="text-end">Akcije</th>
                    </tr>
                </thead>

                <tbody>
                    % for tek in teki:
                        <tr>
                            <td>
                                <span class="fw-semibold">
                                    {{tek.datum.strftime("%d.%m.%Y")}}
                                </span>
                                <div class="text-muted-soft small">
                                    {{tek.datum.strftime("%H:%M")}}
                                </div>
                            </td>

                            <td>
                                <span class="run-value">{{tek.razdalja}} km</span>
                            </td>

                            <td>
                                {{format_trajanje(tek.trajanje)}}
                            </td>

                            <td class="text-end">
                                <a href="{{url('runs/' + str(tek.id) + '/edit')}}" class="btn btn-sm btn-outline-warning me-1">
                                    <i class="bi bi-pencil-square me-1"></i>
                                    Uredi
                                </a>

                                <form method="post" action="{{url('runs/' + str(tek.id) + '/delete')}}" class="d-inline">
                                    <button type="submit" class="btn btn-sm btn-outline-danger" onclick="return confirm('Ali res želite izbrisati ta tek?');">
                                        <i class="bi bi-trash me-1"></i>
                                        Izbriši
                                    </button>
                                </form>
                            </td>
                        </tr>
                    % end
                </tbody>
            </table>
        </div>
    % end
</div>