% rebase("base.tpl", user=user, success=success, error=error)

<h2>Dashboard</h2>

<p>Prijavljen si kot: <b>{{user["uporabnisko_ime"]}}</b></p>
<p>Kovanci: <b>{{user["stanje"]}}</b></p>

<div class="row">
    <div class="col-md-6">
        <div class="card p-3 mb-3">
            <h4>Teki</h4>
            <p>Število tekov: {{len(teki)}}</p>
            <p>Skupna razdalja: {{round(skupna_razdalja, 2)}} km</p>

            <p>
                Skupni čas:
                % if skupno_trajanje >= 60:
                    {{skupno_trajanje // 60}} h {{skupno_trajanje % 60}} min
                % else:
                    {{skupno_trajanje}} min
                % end
            </p>

            <a class="btn btn-primary" href="/runs">Poglej teke</a>
            <a class="btn btn-success" href="/runs/new">Dodaj tek</a>
            <a class="btn btn-warning" href="/strava/connect">Uvozi iz Strave</a>
        </div>
    </div>

    <div class="col-md-6">
        <div class="card p-3 mb-3">
            <h4>Izzivi</h4>
            <p>Število izzivov: {{len(izzivi)}}</p>

            <a class="btn btn-primary" href="/challenges">Poglej izzive</a>
            <a class="btn btn-success" href="/challenges/new">Nov izziv</a>
        </div>
    </div>
</div>