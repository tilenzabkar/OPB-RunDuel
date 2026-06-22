% rebase("base.tpl", user=user, success=success, error=error)

<h2>Lestvica uporabnikov</h2>

<table class="table table-bordered table-striped">
    <thead>
        <tr>
            <th>ID</th>
            <th>Uporabniško ime</th>
            <th>Kovanci</th>
        </tr>
    </thead>

    <tbody>
        % for u in uporabniki:
            <tr>
                <td>{{u.id}}</td>
                <td>{{u.uporabnisko_ime}}</td>
                <td>{{u.stanje}}</td>
            </tr>
        % end
    </tbody>
</table>