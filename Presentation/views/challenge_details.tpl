% rebase("base.tpl", user=user, success=success, error=error)

<div class="page-header mb-4">
    <div>
        <p class="dashboard-eyebrow mb-1">Podrobnosti izziva</p>
        <h2 class="page-title mb-1">Izziv #{{izziv.id}}</h2>
        <p class="text-muted-soft mb-0">
            Tvoj dvoboj proti <strong>{{nasprotnik.uporabnisko_ime}}</strong>
        </p>
    </div>

    <a href="{{url('challenges')}}" class="btn btn-secondary">
        <i class="bi bi-arrow-left me-1"></i>
        Nazaj na izzive
    </a>
</div>

<div class="card challenge-summary-card mb-4">
    <div class="row g-4 align-items-center">
        <div class="col-md-3">
            <div class="summary-label">Nasprotnik</div>
            <div class="summary-value">{{nasprotnik.uporabnisko_ime}}</div>
        </div>

        <div class="col-md-3">
            <div class="summary-label">Vrsta</div>
            <div class="summary-value small-summary">{{lep_izpis_vrste(izziv.vrsta)}}</div>
        </div>

        <div class="col-md-2">
            <div class="summary-label">Stava</div>
            <div class="summary-value">{{izziv.stava}}</div>
            <div class="text-muted-soft small">kovancev</div>
        </div>

        <div class="col-md-2">
            <div class="summary-label">Začetek</div>
            <div class="summary-value small-summary">{{izziv.datum_zacetka.strftime("%d.%m.%Y")}}</div>
            <div class="text-muted-soft small">{{izziv.datum_zacetka.strftime("%H:%M")}}</div>
        </div>

        <div class="col-md-2">
            <div class="summary-label">Konec</div>
            <div class="summary-value small-summary">{{konec.strftime("%d.%m.%Y")}}</div>
            <div class="text-muted-soft small">{{konec.strftime("%H:%M")}}</div>
        </div>
    </div>

    <div class="challenge-status-line mt-4">
        % if izziv.je_zakljucen:
            <span class="status-badge status-done">Zaključen</span>

            % if izziv.zmagovalec:
                <span class="ms-2">
                    Zmagovalec:
                    <strong>{{dobi_uporabnika_po_id(izziv.zmagovalec).uporabnisko_ime}}</strong>
                </span>
            % else:
                <span class="ms-2">Rezultat: <strong>remi</strong></span>
            % end
        % elif izziv.je_sprejet:
            <span class="status-badge status-active">Aktiven</span>
            <span class="ms-2 text-muted-soft">Izziv je sprejet in se štejejo veljavni teki.</span>
        % else:
            <span class="status-badge status-waiting">Čaka na sprejem</span>
            <span class="ms-2 text-muted-soft">Nasprotnik mora izziv še sprejeti.</span>
        % end
    </div>
</div>

<div class="row g-4">
    <div class="col-lg-6">
        <div class="card table-card h-100">
            <div class="d-flex justify-content-between align-items-start mb-3">
                <div>
                    <h4 class="mb-1">Tvoji teki</h4>
                    <p class="text-muted-soft mb-0">Veljavni teki za ta izziv.</p>
                </div>
                <span class="dashboard-badge">Število tekov: {{len(uporabnikovi_teki)}}</span>
            </div>

            % if uporabnikovi_teki:
                <div class="table-responsive">
                    <table class="table table-hover align-middle mb-0">
                        <thead>
                            <tr>
                                <th>Datum</th>
                                <th>Razdalja</th>
                                <th>Trajanje</th>
                            </tr>
                        </thead>

                        <tbody>
                            % for tek in uporabnikovi_teki:
                                <tr>
                                    <td>{{tek.datum.strftime("%d.%m.%Y")}}</td>
                                    <td><span class="run-value">{{tek.razdalja}} km</span></td>
                                    <td>{{format_trajanje(tek.trajanje)}}</td>
                                </tr>
                            % end
                        </tbody>
                    </table>
                </div>

                <div class="result-box mt-3">
                    % if izziv.vrsta == tedenska_razdalja:
                        <span class="summary-label">Skupna razdalja</span>
                        <strong>{{sum(tek.razdalja for tek in uporabnikovi_teki)}} km</strong>
                    % else:
                        <span class="summary-label">Najboljši rezultat</span>
                        % if uporabnik_najboljsi_tek:
                            <strong>{{format_trajanje(uporabnik_najboljsi_tek.trajanje)}}</strong>
                            <div class="text-muted-soft small">
                                {{uporabnik_najboljsi_tek.razdalja}} km,
                                {{uporabnik_najboljsi_tek.datum.strftime("%d.%m.%Y")}}
                            </div>
                        % else:
                            <em>Ni veljavnih tekov v tem obdobju.</em>
                        % end
                    % end
                </div>
            % else:
                <div class="empty-state compact-empty">
                    <div class="empty-icon">
                        <i class="bi bi-activity"></i>
                    </div>
                    <h5>Ni veljavnih tekov</h5>
                    <p class="text-muted-soft mb-0">V obdobju izziva še nimaš ustreznega teka.</p>
                </div>
            % end
        </div>
    </div>

    <div class="col-lg-6">
        <div class="card table-card h-100">
            <div class="d-flex justify-content-between align-items-start mb-3">
                <div>
                    <h4 class="mb-1">Teki nasprotnika</h4>
                    <p class="text-muted-soft mb-0">{{nasprotnik.uporabnisko_ime}}</p>
                </div>
                <span class="dashboard-badge">Število tekov: {{len(nasprotnikovi_teki)}}</span>
            </div>

            % if nasprotnikovi_teki:
                <div class="table-responsive">
                    <table class="table table-hover align-middle mb-0">
                        <thead>
                            <tr>
                                <th>Datum</th>
                                <th>Razdalja</th>
                                <th>Trajanje</th>
                            </tr>
                        </thead>

                        <tbody>
                            % for tek in nasprotnikovi_teki:
                                <tr>
                                    <td>{{tek.datum.strftime("%d.%m.%Y")}}</td>
                                    <td><span class="run-value">{{tek.razdalja}} km</span></td>
                                    <td>{{format_trajanje(tek.trajanje)}}</td>
                                </tr>
                            % end
                        </tbody>
                    </table>
                </div>

                <div class="result-box mt-3">
                    % if izziv.vrsta == tedenska_razdalja:
                        <span class="summary-label">Skupna razdalja</span>
                        <strong>{{sum(tek.razdalja for tek in nasprotnikovi_teki)}} km</strong>
                    % else:
                        <span class="summary-label">Najboljši rezultat</span>
                        % if nasprotnik_najboljsi_tek:
                            <strong>{{format_trajanje(nasprotnik_najboljsi_tek.trajanje)}}</strong>
                            <div class="text-muted-soft small">
                                {{nasprotnik_najboljsi_tek.razdalja}} km,
                                {{nasprotnik_najboljsi_tek.datum.strftime("%d.%m.%Y")}}
                            </div>
                        % else:
                            <em>Nasprotnik nima veljavnih tekov v tem obdobju.</em>
                        % end
                    % end
                </div>
            % else:
                <div class="empty-state compact-empty">
                    <div class="empty-icon">
                        <i class="bi bi-person"></i>
                    </div>
                    <h5>Ni veljavnih tekov</h5>
                    <p class="text-muted-soft mb-0">Nasprotnik v obdobju izziva še nima ustreznega teka.</p>
                </div>
            % end
        </div>
    </div>
</div>