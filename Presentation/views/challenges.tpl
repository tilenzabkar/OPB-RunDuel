% rebase("base.tpl", user=user, success=success, error=error)

<div class="page-header mb-4">
    <div>
        <p class="dashboard-eyebrow mb-1">Tekmovanja</p>
        <h2 class="page-title mb-1">Izzivi</h2>
        <p class="text-muted-soft mb-0">
            Spremljaj odprte, aktivne in zaključene tekaške izzive.
        </p>
    </div>

    <a class="btn btn-primary" href="{{url('challenges/new')}}">
        <i class="bi bi-plus-lg me-1"></i>
        Nov izziv
    </a>
</div>

<div class="card table-card">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h4 class="mb-0">Seznam izzivov</h4>
        <span class="dashboard-badge">Število izzivov: {{len(izzivi)}}</span>
    </div>

    % if len(izzivi) == 0:
        <div class="empty-state">
            <div class="empty-icon">
                <i class="bi bi-trophy"></i>
            </div>
            <h5>Ni še ustvarjenih izzivov</h5>
            <p class="text-muted-soft mb-3">
                Ustvari prvi izziv in povabi prijatelja na tekaški dvoboj.
            </p>
            <a class="btn btn-primary" href="{{url('challenges/new')}}">
                Ustvari prvi izziv
            </a>
        </div>
    % else:
        <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
                <thead>
                    <tr>
                        <th>Nasprotnik</th>
                        <th>Vrsta</th>
                        <th>Stava</th>
                        <th>Začetek</th>
                        <th>Status</th>
                        <th>Zmagovalec</th>
                        <th class="text-end">Akcija</th>
                    </tr>
                </thead>

                <tbody>
                    % for izziv in izzivi:
                        <tr>
                            <td>
                                <div class="fw-bold">
                                    {{ nasprotnik(izziv, user["id"]).uporabnisko_ime }}
                                </div>
                            </td>

                            <td>
                                <span class="challenge-type">
                                    {{lep_izpis_vrste(izziv.vrsta)}}
                                </span>
                            </td>

                            <td>
                                <span class="fw-bold">
                                    {{izziv.stava}}
                                </span>
                                <span class="text-muted-soft small">kovancev</span>
                            </td>

                            <td>
                                <span class="fw-semibold">
                                    {{izziv.datum_zacetka.strftime("%d.%m.%Y")}}
                                </span>
                                <div class="text-muted-soft small">
                                    {{izziv.datum_zacetka.strftime("%H:%M")}}
                                </div>
                            </td>

                            <td>
                                % if izziv.je_zakljucen:
                                    <span class="status-badge status-done">Zaključen</span>
                                % elif izziv.je_sprejet:
                                    <span class="status-badge status-active">Aktiven</span>
                                % else:
                                    <span class="status-badge status-waiting">Čaka</span>
                                % end
                            </td>

                            <td>
                                % if izziv.je_zakljucen:
                                    % if izziv.zmagovalec_ime:
                                        <span class="fw-bold">{{izziv.zmagovalec_ime}}</span>
                                    % else:
                                        <span class="text-muted-soft">Remi</span>
                                    % end
                                % else:
                                    <span class="text-muted-soft">/</span>
                                % end
                            </td>

                            <td class="text-end">
                                <a href="{{url('challenges/' + str(izziv.id))}}" class="btn btn-sm btn-outline-info me-1">
                                    <i class="bi bi-eye me-1"></i>
                                    Podrobnosti
                                </a>

                                % if izziv.je_zakljucen:
                                    <span class="btn btn-sm btn-outline-secondary disabled">
                                        Zaključeno
                                    </span>
                                % elif izziv.je_sprejet:
                                    <form method="post" action="{{url('challenges/' + str(izziv.id) + '/finish')}}" class="d-inline">
                                        <button class="btn btn-sm btn-outline-warning">
                                            Zaključi
                                        </button>
                                    </form>
                                % else:
                                    % if user["id"] == izziv.uporabnik_nasprotuje:
                                        <form method="post" action="{{url('challenges/' + str(izziv.id) + '/accept')}}" class="d-inline">
                                            <button class="btn btn-sm btn-outline-primary">
                                                Sprejmi
                                            </button>
                                        </form>
                                    % elif user["id"] == izziv.uporabnik_stavi:
                                        <span class="btn btn-sm btn-outline-secondary disabled">
                                            Čaka na sprejem
                                        </span>
                                    % else:
                                        <span class="text-muted-soft">-</span>
                                    % end
                                % end
                            </td>
                        </tr>
                    % end
                </tbody>
            </table>
        </div>
    % end
</div>