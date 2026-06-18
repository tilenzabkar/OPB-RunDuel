% rebase("base.tpl", user=user, success=success, error=error)

<h2>Moji teki</h2>

<a class="btn btn-success mb-3" href="/runs/new">Dodaj tek</a>
<a class="btn btn-warning mb-3" href="/strava/connect">Uvozi iz Strave</a>

<table class="table table-bordered table-striped">
    <thead>
        <tr>
            <th>Datum</th>
            <th>Razdalja</th>
            <th>Trajanje</th>
        </tr>
    </thead>

    <tbody>
        % for tek in teki:
            <tr>
                <td>{{tek.datum.strftime("%d.%m.%Y %H:%M")}}</td>

                <td>{{tek.razdalja}} km</td>

                <td>
                    % if tek.trajanje >= 60:
                        {{tek.trajanje // 60}} h {{tek.trajanje % 60}} min
                    % else:
                        {{tek.trajanje}} min
                    % end
                </td>
            </tr>
        % end
    </tbody>
</table>