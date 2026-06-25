% rebase("base.tpl", user=user, success=success, error=error)

<div class="page-header mb-4">
    <div>
        <p class="dashboard-eyebrow mb-1">Nov dvoboj</p>
        <h2 class="page-title mb-1">Ustvari izziv</h2>
        <p class="text-muted-soft mb-0">
            Izberi vrsto izziva, nasprotnika in stavo.
        </p>
    </div>

    <a class="btn btn-secondary" href="{{url('challenges')}}">
        <i class="bi bi-arrow-left me-1"></i>
        Nazaj
    </a>
</div>

<div class="row justify-content-center">
    <div class="col-lg-7">
        <div class="card form-card">
            <form method="post">
                <div class="mb-3">
                    <label class="form-label">Vrsta izziva</label>
                    <select class="form-select form-select-lg" name="vrsta" required>
                        % for tip in tipi:
                            <option value="{{tip.value}}">{{lep_izpis_vrste(tip)}}</option>
                        % end
                    </select>
                </div>

                <div class="mb-3">
                    <label class="form-label">Nasprotnik</label>
                    <select class="form-select form-select-lg" name="nasprotnik_id" required>
                        % for u in uporabniki:
                            <option value="{{u.id}}">
                                {{u.uporabnisko_ime}} — {{u.stanje}} kovancev
                            </option>
                        % end
                    </select>
                </div>

                <div class="coins-info-box mb-3">
                    <div>
                        <div class="summary-label">Tvoje stanje</div>
                        <strong>{{user["stanje"]}} kovancev</strong>
                    </div>
                    <i class="bi bi-coin"></i>
                </div>

                <div class="mb-4">
                    <label class="form-label">Stava</label>
                    <input class="form-control form-control-lg"
                           type="number"
                           name="stava"
                           min="1"
                           max="{{user['stanje']}}"
                           required>
                    <small class="form-text text-muted">
                        Vpiši znesek med 1 in {{user["stanje"]}} kovancev.
                    </small>
                </div>

                <div class="d-flex flex-wrap gap-2">
                    <button class="btn btn-success btn-lg" type="submit">
                        <i class="bi bi-trophy me-1"></i>
                        Ustvari izziv
                    </button>

                    <a class="btn btn-secondary btn-lg" href="{{url('challenges')}}">
                        Prekliči
                    </a>
                </div>
            </form>
        </div>
    </div>
</div>