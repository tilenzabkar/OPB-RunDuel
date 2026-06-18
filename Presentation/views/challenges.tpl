% rebase("base.tpl", user=user, success=success, error=error)

<h2>Izzivi</h2>

<a class="btn btn-success mb-3" href="/challenges/new">Nov izziv</a>

<table class="table table-bordered table-striped">
    <thead>
        <tr>
            <th>Tekmovalca</th>
            <th>Vrsta</th>
            <th>Stava</th>
            <th>Začetek</th>
            <th>Zmagovalec</th>
            <th>Akcija</th>
        </tr>
    </thead>

    <tbody>
        % for izziv in izzivi:
            <tr>
                <td>
                    {{izziv.uporabnik_stavi_ime}}
                    proti
                    {{izziv.uporabnik_nasprotuje_ime}}
                </td>

                <td>{{izziv.vrsta}}</td>
                <td>{{izziv.stava}}</td>

                <td>
                    {{izziv.datum_zacetka.strftime("%d.%m.%Y %H:%M")}}
                </td>

                <td>
                    % if izziv.zmagovalec_ime:
                        {{izziv.zmagovalec_ime}}
                    % else:
                        /
                    % end
                </td>

                <td>
                    % if not izziv.zmagovalec_ime:
                        <form method="post" action="/challenges/{{izziv.id}}/finish">
                            <button class="btn btn-sm btn-warning">Zaključi</button>
                        </form>
                    % else:
                        Zaključeno
                    % end
                </td>
            </tr>
        % end
    </tbody>
</table>