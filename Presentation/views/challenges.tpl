% rebase("base.tpl", user=user, success=success, error=error)

<h2>Izzivi</h2>

<a class="btn btn-success mb-3" href="/challenges/new">Nov izziv</a>

<table class="table table-bordered table-striped">
    <thead>
        <tr>
            <th>Nasprotnik</th>
            <th>Vrsta</th>
            <th>Stava</th>
            <th>Začetek</th>
            <th>Zmagovalec</th>
            <th>Podrobnosti</th>
            <th>Akcija</th>
        </tr>
    </thead>

    <tbody>
        % for izziv in izzivi:
            <tr>
                <td>
                    {{ nasprotnik(izziv, user["id"]).uporabnisko_ime }}
                </td>

                <td>{{izziv.vrsta}}</td>
                <td>{{izziv.stava}}</td>

                <td>
                    {{izziv.datum_zacetka.strftime("%d.%m.%Y %H:%M")}}
                </td>

                <td>
                    % if izziv.je_zakljucen:
                        % if izziv.zmagovalec_ime:
                            {{ izziv.zmagovalec_ime }}
                        % else:
                            Remi
                        % end
                    % else:
                        /
                    % end
                </td>

                <td>
                    <a href="/challenges/{{izziv.id}}" class="btn btn-sm btn-info">Podrobnosti</a>
                </td>
                <td>
                    % if izziv.je_zakljucen:
                        <span class="text-muted">Zaključeno</span>
                    % elif izziv.je_sprejet:
                        <form method="post" action="/challenges/{{izziv.id}}/finish">
                                <button class="btn btn-sm btn-warning">Zaključi</button>
                        </form>
                    % else:
                        % if user["id"] == izziv.uporabnik_nasprotuje:
                            <form method="post" action="/challenges/{{izziv.id}}/accept">
                                <button class="btn btn-sm btn-primary">Sprejmi</button>
                            </form>
                        % elif user["id"] == izziv.uporabnik_stavi:
                            <span class="text-secondary">Čaka na sprejem</span>
                        % else:
                            <span class="text-muted">-</span>
                        % end
                    % end
                </td>
            </tr>
        % end
    </tbody>
</table>