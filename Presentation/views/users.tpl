% rebase("base.tpl", user=user, success=success, error=error)

<div class="leaderboard-hero mb-4">
    <div class="leaderboard-hero-icon">
        <i class="bi bi-trophy-fill"></i>
    </div>

    <div>
        <p class="dashboard-eyebrow mb-1">Lestvica</p>
        <h2 class="page-title mb-1">Leaderboard</h2>
        <p class="text-muted-soft mb-0">
            Najboljši uporabniki po številu kovancev.
        </p>
    </div>
</div>

<div class="card table-card">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h4 class="mb-0">Lestvica uporabnikov</h4>
        <span class="dashboard-badge">Število uporabnikov: {{len(uporabniki)}}</span>
    </div>

    % if len(uporabniki) == 0:
        <div class="empty-state">
            <div class="empty-icon">
                <i class="bi bi-people"></i>
            </div>
            <h5>Ni še uporabnikov</h5>
            <p class="text-muted-soft mb-0">
                Ko se uporabniki registrirajo, se bodo prikazali tukaj.
            </p>
        </div>
    % else:
        <div class="table-responsive">
            <table class="table table-hover align-middle mb-0 leaderboard-table">
                <thead>
                    <tr>
                        <th>Mesto</th>
                        <th>Uporabnik</th>
                        <th class="text-end">Kovanci</th>
                    </tr>
                </thead>

                <tbody>
                    % for i, u in enumerate(uporabniki, start=1):
                        <tr>
                            <td>
                                % if i == 1:
                                    <span class="rank-badge rank-gold">1</span>
                                % elif i == 2:
                                    <span class="rank-badge rank-silver">2</span>
                                % elif i == 3:
                                    <span class="rank-badge rank-bronze">3</span>
                                % else:
                                    <span class="rank-badge">{{i}}</span>
                                % end
                            </td>

                            <td>
                                <div class="leaderboard-user">
                                    <div class="user-avatar">
                                        <i class="bi bi-person-fill"></i>
                                    </div>
                                    <div>
                                        <div class="fw-bold">{{u.uporabnisko_ime}}</div>
                                        % if user and user["id"] == u.id:
                                            <div class="text-muted-soft small">Ti</div>
                                        % end
                                    </div>
                                </div>
                            </td>

                            <td class="text-end">
                                <span class="coin-count">
                                    <i class="bi bi-coin me-1"></i>
                                    {{u.stanje}}
                                </span>
                            </td>
                        </tr>
                    % end
                </tbody>
            </table>
        </div>
    % end
</div>