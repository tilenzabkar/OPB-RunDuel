% rebase("base.tpl", user=user, success=success, error=error)

<h2>Moji teki</h2>

<a class="btn btn-success mb-3" href="/runs/new">Dodaj tek</a>
<a class="btn btn-warning mb-3" href="/strava/connect">Uvozi iz Strave</a>
<a class="btn btn-danger mb-3" href="/strava/logout" target="_blank" rel="noopener noreferrer">Odjava iz Strave</a>

<table class="table table-bordered table-striped">
    <thead>
        <tr>
            <th>Datum</th>
            <th>Razdalja</th>
            <th>Trajanje</th>
            <th>Akcije</th>
        </tr>
    </thead>

    <tbody>
        % for tek in teki:
            <tr>
                <td>{{tek.datum.strftime("%d.%m.%Y %H:%M")}}</td>
                <td>{{tek.razdalja}} km</td>
                <td>{{format_trajanje(tek.trajanje)}}</td>
                <td>
                    <a href="/runs/{{ tek.id }}/edit" class="btn btn-sm btn-warning">
                        <i class="bi bi-pencil-square"></i>
                    </a>
                    
                    <form method="post" action="/runs/{{ tek.id }}/delete" style="display:inline;">
                        <button type="submit" class="btn btn-sm btn-danger" onclick="return confirm('Ali res želite izbrisati ta tek?');">
                            <i class="bi bi-trash"></i>
                        </button>
                    </form>
                </td>
            </tr>
        % end
    </tbody>
</table>