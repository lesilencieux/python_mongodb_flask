# _*_ encoding: utf-8 _*_
import sys

reload(sys)
sys.setdefaultencoding('utf8')

from app import app, lm
from flask import request, redirect, render_template, url_for, flash
from flask.ext.login import login_user, logout_user, login_required
from .forms import LoginForm
from app.models import user
from app.models import structure
from app.models import type_agent
from app.models import qualite
from app.models import corps
from app.models import grade
from app.models import agent
from app.models import budget
from app.models import type_budgets
from app.models import pays
from app.models import ville
from app.models import mission
from .user import User
from werkzeug.security import generate_password_hash
from datetime import datetime


@app.route('/')
def home():
    # return render_template('admin.html')
    return render_template('admin_login.html')


@app.route('/admin1')
def home1():
    return render_template('admin.html')


@app.route('/register')
def register():
    return render_template('admin_register.html')


@app.route('/structures')
def structur():
    return render_template('structures/structures.html')


@app.route('/missions')
def missions():
    agt = agent.Agent()
    list_agents = agt.get_agents()
    budg = type_budgets.TypeBudget()
    list_type_budget = budg.get_type_budgets()
    pay = pays.Pays()
    list_pays = pay.get_payss()

    return render_template('missions/missions.html', ville=ville, list_agents=list_agents,
                           list_type_budget=list_type_budget,
                           list_pays=list_pays)


@app.route('/villes')
def villes():
    pay = pays.Pays()
    list_pays = pay.get_payss()
    return render_template('villes/villes.html', list_pays=list_pays)


@app.route('/pays')
def payss():
    return render_template('pays/pays.html')


@app.route('/budget')
def budgets():
    typ_budg = type_budgets.TypeBudget()
    list_budgets = typ_budg.get_type_budgets()
    return render_template('budgets/budgets.html', list_budgets=list_budgets)


@app.route('/type_budget')
def type_budgetss():
    return render_template('type_budgets/type_budgets.html')


@app.route('/corps')
def corpss():
    return render_template('corps/type_budgets.html')


@app.route('/qualites')
def qualites():
    return render_template('qualites/qualites.html')


@app.route('/types')
def types():
    return render_template('type_agents/type_agents.html')


@app.route('/grades')
def gradess():
    return render_template('grades/grades.html')


@app.route('/list_structure')
def structures():
    structure1 = structure.Structure()
    list_structures = structure1.get_structures()
    return render_template('structures/list_structure.html', list_structures=list_structures)


@app.route('/list_mission')
def missions_list():
    miss1 = mission.Mission()
    list_missions = miss1.get_missions()
    return render_template('missions/list_mission.html', list_missions=list_missions)


@app.route('/list_budget')
def liste_budgets():
    budget1 = budget.Budget()
    list_budgets = budget1.get_budgets()
    return render_template('budgets/list_budget.html', list_budgets=list_budgets)


@app.route('/list_type_budget')
def liste_type_budgets():
    type_budget1 = type_budgets.TypeBudget()
    list_type_budgets = type_budget1.get_type_budgets()
    return render_template('type_budgets/list_type_budget.html', list_type_budgets=list_type_budgets)


@app.route('/list_qualite')
def list_qualite():
    qualite1 = qualite.Qualite()
    list_qualites = qualite1.get_qualites()
    return render_template('qualites/list_qualite.html', list_qualites=list_qualites)


@app.route('/list_pays')
def list_pays():
    pays1 = pays.Pays()
    list_pays = pays1.get_payss()
    return render_template('pays/list_ville.html', list_pays=list_pays)


@app.route('/list_corps')
def list_corps():
    corps1 = corps.Corps()
    list_corps = corps1.get_corpss()
    return render_template('corps/list_type_budget.html', list_corps=list_corps)


@app.route('/list_grade')
def list_grade():
    grade1 = grade.Grade()
    list_grades = grade1.get_grades()
    return render_template('grades/list_grade.html', list_grades=list_grades)


@app.route('/list_agent')
def agents():
    structure1 = structure.Structure()
    list_structures = structure1.get_structures()
    return render_template('agents/list_agent.html', list_structures=list_structures)


@app.route('/list_type_agent')
def type_agents():
    type_agent1 = type_agent.TypeAgent()
    list_type_agents = type_agent1.get_type_agents()
    return render_template('type_agents/list_type_agent.html', list_type_agents=list_type_agents)


@app.route('/structure/<code_structure>')
def structure_by_code(code_structure):
    structure1 = structure.Structure()
    read_structure = structure1.get_structure_by_code(code_structure)
    return render_template('structures/show_destination.html', read_structure=read_structure)


@app.route('/update_structure/<code_structure>')
def update_structure_by_code(code_structure):
    structure1 = structure.Structure()
    read_structure = structure1.get_structure_by_code(code_structure)
    return render_template('structures/edit_destination.html', read_structure=read_structure)


@app.route('/delete_structure/<code_structure>')
def delete_structure_by_code(code_structure):
    structure1 = structure.Structure()
    read_structure = structure1.delete_structure_by_code(code_structure)
    if read_structure:
        flash("La structure a été bien supprimée!", category='success')
        return redirect(request.args.get("structures/list_destination.html") or url_for("list_structure"))
    flash("Oups ! Quelque chose s'est mal passé lors de la suppression", category='error')
    return render_template('structures/list_destination.html', message="ko")

# @app.route('edit_mission/<id_mission>')
# def edite_mission(id_mission):
#     miss = mission.Mission()
#     read_mission = miss.get_mission(id_mission)
#     miss1 = mission.Mission()
#     list_missions = miss1.get_missions()
#     if read_mission is not None:
#         return render_template("missions/edit_mission.html",read_mission=read_mission)
#     flash("Oups ! Quelque chose s'est mal passé lors de la suppression", category='error')
#     return render_template('missions/list_mission.html',list_missions=list_missions)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user_with_username = app.config['USERS_COLLECTION'].find_one({"username": form.username.data})
        user_with_email = app.config['USERS_COLLECTION'].find_one({"email": form.username.data})
        if user_with_email and User.validate_login(user_with_email['password'], form.password.data):
            user_obj = User(str(user_with_email['username']))
            login_user(user_obj)
            flash("Logged in successfully!", category='success')
            return redirect(request.args.get("next") or url_for("write"))
        elif user_with_username and User.validate_login(user_with_username['password'], form.password.data):
            user_obj = User(str(user_with_username['username']))
            login_user(user_obj)
            flash("Logged in successfully!", category='success')
            return redirect(request.args.get("next") or url_for("write"))
        else:
            flash("Wrong username or password!", category='error')
    return render_template('homes.html', title='login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
def save_user():
    username = request.values.get("usernamesignup")
    email = request.values.get("emailsignup")
    password = request.values.get("passwordsignup")
    pass_hash = generate_password_hash(password, method='pbkdf2:sha256')
    u = {"username": username, "email": email, "password": pass_hash}
    user1 = user.User(username)
    if user1.create(u):
        flash("Utilisateur créé avec succès!", category='success')
        return redirect(request.args.get("next") or url_for("write"))
    flash("Ces identifiants ont été déjà utilisés !", category='error')
    return render_template('admin.html', message="ko")


@app.route('/pays', methods=['GET', 'POST'])
def save_pays():
    code_numerique_pays = request.values.get("code_numerique_pays")
    code_alphat1_pays = request.values.get("code_alphat1_pays")
    code_alphat2_pays = request.values.get("code_alphat2_pays")
    libelle_fr_pays = request.values.get("libelle_fr_pays")
    libelle_en_pays = request.values.get("libelle_en_pays")
    pys = {"code_numerique_pays": code_numerique_pays, "code_alphat1_pays": code_alphat1_pays,
           "libelle_fr_pays": libelle_fr_pays, "libelle_en_pays": libelle_en_pays,
           "code_alphat2_pays": code_alphat2_pays}
    ps = pays.Pays()
    if ps.create_new_pays(pys):
        flash("Pays créé avec succès !", category='success')
        return render_template('pays/pays.html', message="ok")
    flash("Ce code numerique a été déjà utilisé !", category='error')
    return render_template('pays/pays.html', message="ko")


@app.route('/villes', methods=['GET', 'POST'])
def save_villes():
    non_ville = request.values.get("non_ville")
    libelle_fr_pays = request.values.get("libelle_fr_pays")
    libelle_en_pays = request.values.get("libelle_en_pays")
    vll = {"non_ville": non_ville,
           "libelle_fr_pays": libelle_fr_pays, "libelle_en_pays": libelle_en_pays, "created_at": datetime.now()}
    vl = ville.Ville()
    if vl.create_new_ville(vll):
        flash("Pays créé avec succès !", category='success')
        return render_template('villes/villes.html', message="ok")
    flash("Quelque chose s'est mal passé lors de la création de la ville !", category='error')
    return render_template('villes/villes.html', message="ko")


@app.route('/structure', methods=['GET', 'POST'])
def save_structure():
    code_structure = request.values.get("code_structure")
    libelle_structure = request.values.get("libelle_structure")
    delegation_structure = request.values.get("delegation_structure")
    delegue_structure = request.values.get("delegue_structure")
    responsable_structure = request.values.get("responsable_structure")
    visa_responsable_structure = request.values.get("visa_responsable_structure")
    action_structure = request.values.get("action_structure")
    structur = {"code_structure": code_structure, "libelle_structure": libelle_structure,
                "delegation_structure": delegation_structure,
                "delegue_structure": delegue_structure, "responsable_structure": responsable_structure,
                "visa_responsable_structure": visa_responsable_structure,
                "action_structure": action_structure, "created_at": datetime.now()}
    structure1 = structure.Structure()
    if structure1.create_new_structure(structur):
        flash("Structure créé avec succès!", category='success')
        return render_template('structures/structures.html', message="ok")
    flash("Ce code de structure a été déjà utilisé !", category='error')
    return render_template('structures/structures.html', message="ko")


@app.route('/agent', methods=['GET', 'POST'])
def save_agent():
    list_corps = corps.Corps().get_corpss()
    list_grade = grade.Grade().get_grades()
    list_qualite = qualite.Qualite().get_qualites()
    list_structure = structure.Structure().get_structures()

    prenom_agent = request.values.get("prenom_agent")
    nom_agent = request.values.get("nom_agent")
    matricule_agent = request.values.get("matricule_agent")
    structure_agent = request.form.get("structure_agent")
    ifu_agent = request.values.get("ifu_agent")
    corps_agent = request.form.get("corps_agent")
    grade_agent = request.form.get("grade_agent")
    qualite_agent = request.form.get("qualite_agent")
    action_agent = request.values.get("qualite_agent")
    agt = {"prenom_agent": prenom_agent, "nom_agent": nom_agent,
           "matricule_agent": matricule_agent,
           "structure_agent": structure_agent, "ifu_agent": ifu_agent,
           "corps_agent": corps_agent, "action_agent": action_agent,
           "grade_agent": grade_agent, "qualite_agent": qualite_agent, "created_at": datetime.now()}
    agent1 = agent.Agent()
    if agent1.create_new_agent(agt):
        flash("Agent créé avec succès!", category='success')
        return render_template('agents/agents.html', message="ok")
    flash("Cet IFU ou le matricule a été déjà utilisé !", category='error')
    return render_template('agents/agents.html', list_corps=list_corps, list_grade=list_grade,
                           list_qualite=list_qualite, list_structure=list_structure)


@app.route('/qualite', methods=['GET', 'POST'])
def save_qualite():
    libelle_qualite = request.values.get("libelle_qualite")
    description_qualite = request.values.get("description_qualite")
    action_qualite = request.values.get("action_qualite")

    qualit = {"libelle_qualite": libelle_qualite, "description_qualite": description_qualite,
              "action_qualite": action_qualite, "created_at": datetime.now()}
    qualite1 = qualite.Qualite()
    if qualite1.create_new_qualite(qualit):
        flash("Qualité créé avec succès!", category='success')
        return render_template('qualites/qualites.html', message="ok")
    flash("Ce libelle de qualité a été déjà utilisé !", category='error')
    return render_template('qualites/qualites.html', message="ko")


@app.route('/type_agent', methods=['GET', 'POST'])
def save_type_agent():
    libelle_type_agent = request.values.get("libelle_type_agent")
    libelle_unique_type_agent = request.values.get("libelle_unique_type_agent")
    description_type_agent = request.values.get("description_type_agent")
    action_type_agent = request.values.get("action_type_agent")

    typ_agent = {"libelle_type_agent": libelle_type_agent, "libelle_unique_type_agent": libelle_unique_type_agent,
                 "description_type_agent": description_type_agent,
                 "action_type_agent": action_type_agent, "created_at": datetime.now()}
    typ_agent1 = type_agent.TypeAgent()
    if typ_agent1.create_new_type_agent(typ_agent):
        flash("Structure créé avec succès!", category='success')
        return render_template('agents/agents.html', message="ok")
    flash("Ce libelle du type agent a été déjà utilisé !", category='error')
    return render_template('agents/agents.html', message="ko")


@app.route('/type_budget', methods=['GET', 'POST'])
def save_type_budget():
    libelle_type_budget = request.values.get("libelle_type_budget")
    libelle_unique_type_budget = request.values.get("libelle_unique_type_budget")
    description_type_budget = request.values.get("description_type_budget")
    action_type_budget = request.values.get("action_type_budget")

    type_budgt = {"libelle_type_budget": libelle_type_budget, "libelle_unique_type_budget": libelle_unique_type_budget,
                  "description_type_budget": description_type_budget,
                  "action_type_budget": action_type_budget, "created_at": datetime.now()}
    typ_budget1 = type_budgets.TypeBudget()
    if typ_budget1.create_new_type_budget(type_budgt):
        flash("Type Budget créé avec succès!", category='success')
        return render_template('type_budgets/type_budgets.html', message="ok")
    flash("Ce libelle du type budget a été déjà utilisé !", category='error')
    return render_template('type_budgets/type_budgets.html', message="ko")


@app.route('/mission', methods=['GET', 'POST'])
def save_missions():
    agt = agent.Agent()
    list_agents = agt.get_agents()
    typ_budg = type_budgets.TypeBudget()
    list_type_budget = typ_budg.get_type_budgets()
    pay = pays.Pays()
    list_pays = pay.get_payss()

    date_debut_mission = request.values.get("date_debut_mission")
    date_fin_mission = request.values.get("date_fin_mission")
    responsable_structure = request.values.get("responsable_structure")
    objet_mission = request.values.get("objet_mission")
    destination_mission = request.values.get("destination_mission")
    reference_ordre_mission = request.values.get("reference_ordre_mission")
    responsable_structure = request.values.get("responsable_structure")
    type_budget = request.form.get("type_budget")
    montant_budget_mission = request.values.get("montant_budget_mission")
    devise_budget = request.form.get("devise_budget")
    date_depart_mission = request.values.get("date_depart_mission")
    date_retour_mission = request.values.get("date_retour_mission")
    pays_destination_mission = request.form.get("pays_destination_mission")
    ville_pays_destination_mission = request.form.get("ville_pays_destination_mission")
    agents_mission = request.form.get("agents_mission")
    moyen_transport_mission = request.values.get("moyen_transport_mission")
    commune_mission = request.values.get("commune_mission")
    immatriculation_moyen_transport_mission = request.values.get("immatriculation_moyen_transport_mission")
    structure_initiatrice_mission = request.values.get("structure_initiatrice_mission")
    code_type_localite_mission = request.values.get("code_type_localite_mission")
    libelle_localite_mission = request.values.get("libelle_localite_mission")
    code_localite_parente_mission = request.values.get("code_localite_parente_mission")
    code_localite_mission = request.values.get("code_localite_mission")

    to_save_mission = {"date_debut_mission": date_debut_mission, "date_fin_mission": date_fin_mission,
                       "responsable_structure": responsable_structure,
                       "code_localite_mission": code_localite_mission,
                       "code_localite_parente_mission": code_localite_parente_mission,
                       "libelle_localite_mission": libelle_localite_mission,
                       "code_type_localite_mission": code_type_localite_mission,
                       "structure_initiatrice_mission": structure_initiatrice_mission,
                       "immatriculation_moyen_transport_mission": immatriculation_moyen_transport_mission,
                       "commune_mission": commune_mission,
                       "moyen_transport_mission": moyen_transport_mission,
                       "agents_mission": agents_mission,
                       "ville_pays_destination_mission": ville_pays_destination_mission,
                       "pays_destination_mission": pays_destination_mission,
                       "date_retour_mission": date_retour_mission,
                       "date_depart_mission": date_depart_mission,
                       "devise_budget": devise_budget,
                       "responsable_structure": responsable_structure,
                       "montant_budget_mission": montant_budget_mission,
                       "objet_mission": objet_mission, "destination_mission": destination_mission,
                       "reference_ordre_mission": reference_ordre_mission,
                       "created_at" : datetime.now(),
                       "status_mission" :"En attente de validation",
                       "auteur" :"Hilaire"
                        }
    missi = mission.Mission()
    if missi.create_new_mission(to_save_mission):
        flash("Mission créé avec succès!", category='success')
        return render_template('missions/missions.html', list_agents=list_agents, list_pays=list_pays,
                               list_type_budget=list_type_budget)
    flash("Quelque chose s'est mal passé lors de la création de la mission !", category='error')
    return render_template('missions/missions.html', list_agents=list_agents, list_pays=list_pays,
                           list_type_budget=list_type_budget)

@app.route('/update_mission/<id_mission>', methods=['GET', 'POST'])
def update_missions(id_mission):
    agt = agent.Agent()
    list_agents = agt.get_agents()
    typ_budg = type_budgets.TypeBudget()
    list_type_budget = typ_budg.get_type_budgets()
    pay = pays.Pays()
    list_pays = pay.get_payss()

    date_debut_mission = request.values.get("date_debut_mission")
    date_fin_mission = request.values.get("date_fin_mission")
    responsable_structure = request.values.get("responsable_structure")
    objet_mission = request.values.get("objet_mission")
    destination_mission = request.values.get("destination_mission")
    reference_ordre_mission = request.values.get("reference_ordre_mission")
    responsable_structure = request.values.get("responsable_structure")
    type_budget = request.form.get("type_budget")
    montant_budget_mission = request.values.get("montant_budget_mission")
    devise_budget = request.form.get("devise_budget")
    date_depart_mission = request.values.get("date_depart_mission")
    date_retour_mission = request.values.get("date_retour_mission")
    pays_destination_mission = request.form.get("pays_destination_mission")
    ville_pays_destination_mission = request.form.get("ville_pays_destination_mission")
    agents_mission = request.form.get("agents_mission")
    moyen_transport_mission = request.values.get("moyen_transport_mission")
    commune_mission = request.values.get("commune_mission")
    immatriculation_moyen_transport_mission = request.values.get("immatriculation_moyen_transport_mission")
    structure_initiatrice_mission = request.values.get("structure_initiatrice_mission")
    code_type_localite_mission = request.values.get("code_type_localite_mission")
    libelle_localite_mission = request.values.get("libelle_localite_mission")
    code_localite_parente_mission = request.values.get("code_localite_parente_mission")
    code_localite_mission = request.values.get("code_localite_mission")

    to_update_mission = {"date_debut_mission": date_debut_mission, "date_fin_mission": date_fin_mission,
                       "responsable_structure": responsable_structure,
                       "code_localite_mission": code_localite_mission,
                       "code_localite_parente_mission": code_localite_parente_mission,
                       "libelle_localite_mission": libelle_localite_mission,
                       "code_type_localite_mission": code_type_localite_mission,
                       "structure_initiatrice_mission": structure_initiatrice_mission,
                       "immatriculation_moyen_transport_mission": immatriculation_moyen_transport_mission,
                       "commune_mission": commune_mission,
                       "moyen_transport_mission": moyen_transport_mission,
                       "agents_mission": agents_mission,
                       "ville_pays_destination_mission": ville_pays_destination_mission,
                       "pays_destination_mission": pays_destination_mission,
                       "date_retour_mission": date_retour_mission,
                       "date_depart_mission": date_depart_mission,
                       "devise_budget": devise_budget,
                       "responsable_structure": responsable_structure,
                       "montant_budget_mission": montant_budget_mission,
                       "objet_mission": objet_mission, "destination_mission": destination_mission,
                       "reference_ordre_mission": reference_ordre_mission}
    missi = mission.Mission()
    if missi.update_mission(id_mission,to_update_mission):
        flash("Mission mise à jour avec succès!", category='success')
        return render_template('missions/missions.html', list_agents=list_agents, list_pays=list_pays,
                               list_type_budget=list_type_budget)
    flash("Quelque chose s'est mal passé lors de la mise à jour de la mission !", category='error')
    return render_template('missions/missions.html', list_agents=list_agents, list_pays=list_pays,
                           list_type_budget=list_type_budget)


@app.route('/budget', methods=['GET', 'POST'])
def save_budget():
    type_budget1 = type_budgets.TypeBudget()
    list_type_budgets = type_budget1.get_type_budgets()
    libelle_budget = request.values.get("libelle_budget")
    type_budget = request.form.get("type_budget")
    action_budget = request.values.get("action_budget")

    type_budgt = {"libelle_budget": libelle_budget, "type_budget": type_budget,
                  "action_budget": action_budget, "created_at": datetime.now()}
    typ_budget1 = budget.Budget()
    if typ_budget1.create_new_budget(type_budgt):
        flash("Budget créé avec succès!", category='success')
        return render_template('budgets/budgets.html', list_type_budgets=list_type_budgets)
    flash("Ce libelle du budget a été déjà utilisé !", category='error')
    return render_template('budgets/budgets.html', list_type_budgets=list_type_budgets)


@app.route('/pays_select', methods=['GET', 'POST'])
def get_city_by_country():
    list_countries = request.form.get("pays_destination_mission")
    print("list_countries >>>>>>>>>>>" + list_countries)
    list_cities_of_each_country = ville.Ville().get_all_cities_for_countries(list_countries)
    print("list_cities_of_each_country >>>>>>>>>>>" + list_cities_of_each_country)

    if list_cities_of_each_country is not None:
        return render_template('missions/missions.html', list_cities_of_each_country=list_cities_of_each_country)


@app.route('/corps', methods=['GET', 'POST'])
def save_corps():
    libelle_corps = request.values.get("libelle_corps")
    action_corps = request.values.get("action_corps")

    crps = {"libelle_corps": libelle_corps, "action_corps": action_corps
        , "created_at": datetime.now()}
    crps1 = corps.Corps()
    if crps1.create_new_corps(crps):
        flash("Corps créé avec succès!", category='success')
        return render_template('corps/type_budgets.html', message="ok")
    flash("Ce libelle du type agent a été déjà utilisé !", category='error')
    return render_template('corps/type_budgets.html', message="ko")


@app.route('/grade', methods=['GET', 'POST'])
def save_grade():
    libelle_grade = request.values.get("libelle_grade")
    action_grade = request.values.get("action_grade")

    grad = {"libelle_grade": libelle_grade, "action_grade": action_grade
        , "created_at": datetime.now()}
    grad1 = grade.Grade()
    if grad1.create_new_grade(grad):
        flash("Grade créé avec succès!", category='success')
        return render_template('grades/grades.html', message="ok")
    flash("Ce libelle du grade a été déjà utilisé !", category='error')
    return render_template('grades/grades.html', message="ko")


@app.route('/mission/<id_mission>')
def read_mission_by_id(id_mission):
    miss = mission.Mission()
    read_mission = miss.get_mission(id_mission)
    return render_template('missions/show_mission.html', read_mission=read_mission)


@app.route('/validate_mission/<id_mission>')
def validate_mission(id_mission):
    miss1 = mission.Mission()
    list_missions = miss1.get_missions()
    if mission.Mission().validate_mission(id_mission):
        flash("Mission vaildée avec succès!", category='success')
        return render_template('missions/list_mission.html',list_missions=list_missions)
    flash("Quelque chose s'est mal passé lors de la validation de la mission !", category='error')
    return render_template('missions/list_mission.html',list_missions=list_missions)


@app.route('/delete_mission/<id_mission>')
def delete_mission(id_mission):
    miss1 = mission.Mission()
    list_missions = miss1.get_missions()
    if mission.Mission().delete_mission(str(id_mission)):
        flash("Mission supprimée avec succès!", category='success')
        return render_template('missions/list_mission.html',list_missions=list_missions)
    flash("Quelque chose s'est mal passé lors de la suppression de la mission !", category='error')
    return render_template('missions/list_mission.html',list_missions=list_missions)


@app.route('/write', methods=['GET', 'POST'])
@login_required
def write():
    return render_template('write.html')


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    return render_template('settings.html')


@lm.user_loader
def load_user(username):
    u = app.config['USERS_COLLECTION'].find_one({"_id": username})
    if not u:
        return None
    return user.User(u['_id'])
