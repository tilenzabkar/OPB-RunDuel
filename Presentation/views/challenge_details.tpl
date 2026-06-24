% rebase("base.tpl", user=user, success=success, error=error)

<h2>Podrobnosti izziva #{{izziv.id}}</h2>

<div class="card mb-4">
    <div class="card-body">
        <p><strong>Nasprotnik:</strong> {{ nasprotnik.uporabnisko_ime }}</p>
        <p><strong>Vrsta:</strong> {{ lep_izpis_vrste(izziv.vrsta) }}</p>
        <p><strong>Stava:</strong> {{izziv.stava}} kovancev</p>
        <p><strong>Začetek:</strong> {{izziv.datum_zacetka.strftime("%d.%m.%Y %H:%M")}}</p>
        <p><strong>Konec:</strong> {{ konec.strftime("%d.%m.%Y %H:%M") }}</p>
        <p><strong>Status:</strong> 
            % if izziv.je_zakljucen:
                Zaključen
                % if izziv.zmagovalec:
                    (zmagovalec: {{ dobi_uporabnika_po_id(izziv.zmagovalec).uporabnisko_ime }})
                % else:
                    (remi)
                % end
            % elif izziv.je_sprejet:
                Aktiven
            % else:
                Čaka na sprejem
            % end
        </p>
    </div>
</div>

<div class="row">
    <div class="col-md-6">
        <h4>Tvoji veljavni teki za izziv:</h4>
        % if uporabnikovi_teki:
            <table class="table table-sm table-bordered">
                <thead>
                    <tr><th>Datum</th><th>Razdalja (km)</th><th>Trajanje</th></tr>
                </thead>
                <tbody>
                % for tek in uporabnikovi_teki:
                    <tr>
                        <td>{{tek.datum.strftime("%d.%m.%Y")}}</td>
                        <td>{{tek.razdalja}}</td>
                        <td>{{format_trajanje(tek.trajanje)}}</td>
                    </tr>
                % end
                </tbody>
            </table>
            % if izziv.vrsta == tedenska_razdalja:
                <p><strong>Skupna razdalja:</strong> {{sum(tek.razdalja for tek in uporabnikovi_teki)}} km</p>
            % else:
                <p><strong>Najboljši rezultat:</strong> 
                    % if uporabnik_najboljsi_tek:
                        {{format_trajanje(uporabnik_najboljsi_tek.trajanje)}} 
                        ({{uporabnik_najboljsi_tek.razdalja}} km, {{uporabnik_najboljsi_tek.datum.strftime("%d.%m.%Y")}})
                    % else:
                        <p><em>Ni veljavnih tekov v tem obdobju.</em></p>
                    % end
                </p>
            % end
        % else:
            <p><em>Ni veljavnih tekov v tem obdobju.</em></p>
        % end
    </div>

    <div class="col-md-6">
        <h4>Veljavni teki nasprotnika ({{nasprotnik.uporabnisko_ime}})</h4>
        % if nasprotnikovi_teki:
            <table class="table table-sm table-bordered">
                <thead>
                    <tr><th>Datum</th><th>Razdalja (km)</th><th>Trajanje</th></tr>
                </thead>
                <tbody>
                % for tek in nasprotnikovi_teki:
                    <tr>
                        <td>{{tek.datum.strftime("%d.%m.%Y")}}</td>
                        <td>{{tek.razdalja}}</td>
                        <td>{{format_trajanje(tek.trajanje)}}</td>
                    </tr>
                % end
                </tbody>
            </table>
            % if izziv.vrsta == tedenska_razdalja:
                <p><strong>Skupna razdalja:</strong> {{sum(tek.razdalja for tek in nasprotnikovi_teki)}} km</p>
            % else:
                <p><strong>Najboljši rezultat nasprotnika:</strong> 
                    % if nasprotnik_najboljsi_tek:
                        {{format_trajanje(nasprotnik_najboljsi_tek.trajanje)}} 
                        ({{nasprotnik_najboljsi_tek.razdalja}} km, {{nasprotnik_najboljsi_tek.datum.strftime("%d.%m.%Y")}})
                    % else:
                        <p><em>Nasprotnik nima veljavnih tekov v tem obdobju.</em></p>
                    % end
                </p>
            % end
        % else:
            <p><em>Nasprotnik nima veljavnih tekov v tem obdobju.</em></p>
        % end
    </div>

<a href="{{url('challenges')}}" class="btn btn-secondary">Nazaj na seznam</a>