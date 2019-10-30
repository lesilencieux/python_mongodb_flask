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
from app.models import users
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from datetime import datetime
import dateutil.parser


@app.route('/')
def home():
    return render_template('admin_login.html')
    # return render_template('admin.html')


@app.template_filter()
def datetimefilter(value, format='%Y/%m/%d %H:%M'):
    """convert a datetime to a different format."""
    return value.strftime(format)


app.jinja_env.filters['datetimefilter'] = datetimefilter


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

    struc = structure.Structure()
    list_structures = struc.get_structures()

    return render_template('missions/missions.html', ville=ville, list_agents=list_agents,
                           list_type_budget=list_type_budget,
                           list_pays=list_pays, list_structures=list_structures)


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
    return render_template('corps/corps.html')


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
    return render_template('pays/list_pays.html', list_pays=list_pays)


@app.route('/list_corps')
def list_corps():
    corps1 = corps.Corps()
    list_corps = corps1.get_corpss()
    return render_template('corps/list_corps.html', list_corps=list_corps)


@app.route('/list_grade')
def list_grade():
    grade1 = grade.Grade()
    list_grades = grade1.get_grades()
    return render_template('grades/list_grade.html', list_grades=list_grades)


@app.route('/list_agent')
def agents():
    agent1 = agent.Agent()
    list_agents = agent1.get_agents()
    return render_template('agents/list_agent.html', list_agents=list_agents)


@app.route('/show_agent/<id_agent>')
def show_agents(id_agent):
    agent1 = agent.Agent()
    list_agent = agent1.get_agent(str(id_agent))
    print(list_agent)
    return render_template('agents/show_agent.html', list_agent=list_agent)


@app.route('/show_grade/<id_grade>')
def show_grade(id_grade):
    grade1 = grade.Grade()
    read_grade = grade1.get_grade(str(id_grade))
    return render_template('grades/show_grade.html', read_grade=read_grade)


@app.route('/show_corps/<id_corpq>')
def show_corps(id_corpq):
    corps1 = corps.Corps()
    read_corps = corps1.get_corps(str(id_corpq))

    return render_template('corps/show_corps.html', read_corps=read_corps)


@app.route('/show_type_agent/<id_type_agent>')
def show_type_agents(id_type_agent):
    type_agent1 = type_agent.TypeAgent()
    read_type_agent = type_agent1.get_type_agent(str(id_type_agent))
    return render_template('type_agents/show_type_agent.html', read_type_agent=read_type_agent)


@app.route('/show_qualite/<id_qualite>')
def show_qualite(id_qualite):
    qualite1 = qualite.Qualite()
    read_qualite = qualite1.get_qualite(str(id_qualite))
    print(read_qualite)
    return render_template('qualites/show_qualite.html', read_qualite=read_qualite)


@app.route('/delete_agent/<id_agent>')
def delete_agents(id_agent):
    agent1 = agent.Agent()
    agent1.delete_agent(str(id_agent))
    list_agents = agent1.get_agents()
    return render_template('agents/list_agent.html', list_agents=list_agents)


@app.route('/list_type_agent')
def type_agents():
    type_agent1 = type_agent.TypeAgent()
    list_type_agents = type_agent1.get_type_agents()
    return render_template('type_agents/list_type_agent.html', list_type_agents=list_type_agents)


@app.route('/structure/<id_structure>')
def structure_by_id(id_structure):
    structure1 = structure.Structure()
    read_structure = structure1.get_structure(str(id_structure))
    return render_template('structures/show_structure.html', read_structure=read_structure)


@app.route('/update_structure/<id>')
def update_structure_by_code(id):
    structure1 = structure.Structure()
    read_structure = structure1.get_structure(str(id))
    return render_template('structures/edit_structure.html', read_structure=read_structure)


@app.route('/update_type_agent/<id>')
def update_type_agent(id):
    type_agent1 = type_agent.TypeAgent()
    read_type_agent = type_agent1.get_type_agent(str(id))
    return render_template('type_agents/edit_type_agent.html', read_type_agent=read_type_agent)


@app.route('/update_qualite/<id>')
def update_qualite(id):
    qualite1 = qualite.Qualite()
    read_qualite = qualite1.get_qualite(str(id))
    return render_template('qualites/edit_qualite.html', read_qualite=read_qualite)


@app.route('/update_corps/<id>')
def update_corps(id):
    corps1 = corps.Corps()
    read_corps = corps1.get_corps(str(id))
    return render_template('corps/edit_corps.html', read_corps=read_corps)


@app.route('/update_grade/<id>')
def update_grade(id):
    grade1 = grade.Grade()
    read_grade = grade1.get_grade(str(id))
    return render_template('grades/edit_grade.html', read_grade=read_grade)


@app.route('/delete_structure/<id>')
def delete_structure_by_id(id):
    structure1 = structure.Structure()
    list_structures = structure1.get_structures()
    read_structure = structure1.deleteStructure(str(id))
    if read_structure:
        flash("La structure a été bien supprimée!", category='success')
        return render_template('structures/list_structure.html', list_structures=list_structures)
    flash("Oups ! Quelque chose s'est mal passé lors de la suppression", category='error')
    return render_template('structures/list_structure.html', message="ko")


@app.route('/delete_type_budget/<id>')
def delete_type_budget_by_id(id):
    type_budgets1 = type_budgets.TypeBudget()
    read_structure = type_budgets1.deletetype_budget(id)

    list_type_budgets = type_budgets1.get_type_budgets()
    if read_structure:
        flash("Type budget supprimé avec succès", category='success')
        return render_template('type_bugets/list_type_budget.html', list_type_budgets=list_type_budgets)
    else:
        flash("Oups ! Quelque chose s'est mal passé lors de la suppression du type de budget", category='error')
        return render_template('type_bugets/list_type_budget.html', list_type_budgets=list_type_budgets)


@app.route('/delete_pays/<id>')
def delete_pays_by_id(id):
    pays1 = pays.Pays()
    read_pays = pays1.delete_pays(id)

    list_pays2 = pays1.get_payss()
    if read_pays:
        flash("Pays supprimé avec succès", category='success')
        return render_template('pays/list_pays.html', list_pays=list_pays2)
    else:
        flash("Oups ! Quelque chose s'est mal passé lors de la suppression du pays", category='error')
        return render_template('pays/list_pays.html', list_pays=list_pays2)


@app.route('/delete_type_agent/<id>')
def delete_type_agent(id):
    type_agent1 = type_agent.TypeAgent()
    read_pays = type_agent1.delete_type_agent(id)

    list_type_agent2 = type_agent1.get_type_agents()
    if read_pays:
        flash("Type agent supprimé avec succès", category='success')
        return render_template('type_agents/list_type_agent.html', list_type_agents=list_type_agent2)
    else:
        flash("Oups ! Quelque chose s'est mal passé lors de la suppression du type agent", category='error')
        return render_template('type_agents/list_type_agent.html', list_type_agents=list_type_agent2)


@app.route('/delete_ville/<id>')
def delete_ville_by_id(id):
    v1 = ville.Ville()
    read_ville = v1.delete_ville(id)

    list_ville2 = v1.get_villes()
    if read_ville:
        flash("Ville supprimée avec succès", category='success')
        return render_template('villes/list_ville.html', list_ville=list_ville2)
    else:
        flash("Oups ! Quelque chose s'est mal passé lors de la suppression de la ville", category='error')
        return render_template('villes/list_ville.html', list_ville=list_ville2)


@app.route('/delete_structure/<code_structure>')
def delete_structure_by_code(code_structure):
    structure1 = structure.Structure()
    read_structure = structure1.delete_structure_by_code(code_structure)
    if read_structure:
        flash("La structure a été bien supprimée!", category='success')
        return redirect(request.args.get("structures/list_structure.html") or url_for("list_structure"))
    flash("Oups ! Quelque chose s'est mal passé lors de la suppression", category='error')
    return render_template('structures/list_structure.html', message="ko")


@app.route('/login', methods=['GET', 'POST'])
def login():
    miss1 = mission.Mission()
    list_missions = miss1.get_missions()
    if request.method == 'POST':
        user_with_username = users.Users("", "").login_user_with_username(request.values.get("username"))
        user_with_email = users.Users("", "").login_user_with_email(request.values.get("email"))
        password = request.values.get("password")
        if user_with_email:
            read_user1 = users.Users("", "").get_user_by_email(request.values.get("email"))
            if user_with_email and check_password_hash(read_user1['password'], password):
                login_user(users.Users(read_user1['username'], ""))
                return render_template('missions/list_mission.html', user=read_user1, list_missions=list_missions)
            flash("Wrong username or password!", category='error')
            # return render_template('admin.html')
            return render_template('admin_login.html')
        elif user_with_username:
            read_user2 = users.Users("", "").get_user_by_username(request.values.get("username"))
            if user_with_username and check_password_hash(read_user2['password'], password):
                login_user(users.Users(read_user2['username'], ""))
                print(read_user2)
                return render_template('missions/list_mission.html', user=read_user2, list_missions=list_missions)
            flash("Nom d'utilisateur ou Mot de passe incorrect !", category='error')
            # return render_template('admin.html')
            return render_template('admin_login.html')
        else:
            flash("Nom d'utilisateur ou Mot de passe incorrect !", category='error')
    # return render_template('admin.html')
    return render_template('admin_login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
def save_users():
    username = request.values.get("usernamesignup")
    email = request.values.get("emailsignup")
    password = request.values.get("passwordsignup")
    print(password)
    u = {"username": username, "email": email, "password": generate_password_hash(password, method='pbkdf2:sha256'),
         "roles": ["admin", "invite"]}
    user1 = users.Users("", "")
    if username is not None and email is not None and password is not None:
        if user1.create_new_users(u):
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


@app.route('/list_ville')
def list_villes():
    vl = ville.Ville()
    list_ville = vl.get_villes()
    return render_template('villes/list_ville.html', list_ville=list_ville)


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


@app.route('/structure_update/<id>', methods=['GET', 'POST'])
def structure_update(id):
    type_agent1 = type_agent.TypeAgent()
    read_type_agent = type_agent1.get_type_agent(str(id))

    libelle_structure = request.values.get("libelle_structure")
    delegation_structure = request.values.get("delegation_structure")
    delegue_structure = request.values.get("delegue_structure")
    responsable_structure = request.values.get("responsable_structure")
    visa_responsable_structure = request.values.get("visa_responsable_structure")
    structur = {"libelle_structure": libelle_structure,
                "delegation_structure": delegation_structure,
                "delegue_structure": delegue_structure, "responsable_structure": responsable_structure,
                "visa_responsable_structure": visa_responsable_structure, "created_at": datetime.now()}
    structure1 = structure.Structure()
    if structure1.update_structure(str(id), structur):
        flash("Structure mise à jour avec succès!", category='success')
        return render_template('structures/structures.html', read_type_agent=read_type_agent)
    flash("Quelque chose s'est mal passé lors de la mise à jour de la structure", category='error')
    return render_template('structures/structures.html', read_type_agent=read_type_agent)


@app.route('/agent', methods=['GET', 'POST'])
def save_agent():
    list_grades = grade.Grade().get_grades()
    list_qualities = qualite.Qualite().get_qualites()
    list_structures = structure.Structure().get_structures()
    corps_list = corps.Corps().get_corpss()
    prenom_agent = request.values.get("prenom_agent")
    nom_agent = request.values.get("nom_agent")
    matricule_agent = request.values.get("matricule_agent")
    structure_agent = request.form.get("structure_agent")
    ifu_agent = request.values.get("ifu_agent")
    date_et_lieu_de_naissance_agent = request.values.get("date_et_lieu_de_naissance_agent")
    corps_agent = request.form.get("corps_agent")
    grade_agent = request.form.get("grade_agent")
    qualite_agent = request.form.get("qualite_agent")
    agt = {"prenom_agent": prenom_agent, "nom_agent": nom_agent,
           "matricule_agent": matricule_agent,
           "structure_agent": structure_agent, "ifu_agent": ifu_agent,
           "corps_agent": corps_agent,
           "date_et_lieu_de_naissance_agent": date_et_lieu_de_naissance_agent,
           "grade_agent": grade_agent, "qualite_agent": qualite_agent, "created_at": datetime.now()}
    agent1 = agent.Agent()
    if prenom_agent is not None and nom_agent is not None and matricule_agent is not None and ifu_agent is not None:
        if agent1.create_new_agent(agt):
            flash("Agent créé avec succès!", category='success')
            return render_template('agents/agents.html', corps_list=corps_list, list_grades=list_grades,
                                   list_qualities=list_qualities, list_structures=list_structures)

    return render_template('agents/agents.html', corps_list=corps_list, list_grades=list_grades,
                           list_qualities=list_qualities, list_structures=list_structures)


@app.route('/qualite', methods=['GET', 'POST'])
def save_qualite():
    libelle_qualite = request.values.get("libelle_qualite")
    description_qualite = request.values.get("description_qualite")
    action_qualite = request.values.get("action_qualite")

    qualit = {"libelle_qualite": libelle_qualite, "description_qualite": description_qualite,
              "action_qualite": action_qualite, "created_at": datetime.now()}
    qualite1 = qualite.Qualite()
    if libelle_qualite is not None and description_qualite is not None:
        if qualite1.create_new_qualite(qualit):
            flash("Qualité créé avec succès!", category='success')
            return render_template('qualites/qualites.html', message="ok")
        flash("Ce libelle de qualité a été déjà utilisé !", category='error')
        return render_template('qualites/qualites.html', message="ko")

    return render_template('qualites/qualites.html', message="ko")


@app.route('/qualite_update/<id_qualite>', methods=['GET', 'POST'])
def qualite_update(id_qualite):
    qualite1 = qualite.Qualite()
    read_qualite = qualite1.get_qualite(str(id))

    libelle_qualite = request.values.get("libelle_qualite")
    description_qualite = request.values.get("description_qualite")

    qualit = {"libelle_qualite": libelle_qualite, "description_qualite": description_qualite,
              "created_at": datetime.now()}
    qualite1 = qualite.Qualite()
    if libelle_qualite is not None and description_qualite is not None:
        if qualite1.update_qualite(str(id_qualite), qualit):
            flash("Qualité mise à jour avec succès!", category='success')
            return render_template('qualites/qualites.html', read_qualite=read_qualite)
        flash("Oups quelque chose s'est mal passé lors de la mise à jour de la qualité !", category='error')
        return render_template('qualites/edit_qualites.html', read_qualite=read_qualite)
    return render_template('qualites/edit_qualites.html', read_qualite=read_qualite)


@app.route('/type_agent', methods=['GET', 'POST'])
def save_type_agent():
    libelle_type_agent = request.values.get("libelle_type_agent")
    libelle_unique_type_agent = request.values.get("libelle_unique_type_agent")
    description_type_agent = request.values.get("description_type_agent")

    typ_agent = {"libelle_type_agent": libelle_type_agent, "libelle_unique_type_agent": libelle_unique_type_agent,
                 "description_type_agent": description_type_agent,
                 "created_at": datetime.now()}
    typ_agent1 = type_agent.TypeAgent()
    if libelle_type_agent is not None and libelle_unique_type_agent is not None and description_type_agent is not None:
        if typ_agent1.create_new_type_agent(typ_agent):
            flash("Structure créé avec succès!", category='success')
            return render_template('agents/agents.html', message="ok")
        flash("Ce libelle du type agent a été déjà utilisé !", category='error')
        return render_template('agents/agents.html', message="ko")
    return render_template('agents/agents.html', message="ko")


@app.route('/type_agent_update/<id_type_agent>', methods=['GET', 'POST'])
def type_agent_update(id_type_agent):
    type_agent1 = type_agent.TypeAgent()
    read_type_agent = type_agent1.get_type_agent(str(id_type_agent))

    libelle_type_agent = request.values.get("libelle_type_agent")
    description_type_agent = request.values.get("description_type_agent")
    action_type_agent = request.values.get("action_type_agent")

    typ_agent = {"libelle_type_agent": libelle_type_agent,
                 "description_type_agent": description_type_agent,
                 "action_type_agent": action_type_agent, "created_at": datetime.now()}
    typ_agent1 = type_agent.TypeAgent()
    if typ_agent1.updatetype_agent(str(id_type_agent), typ_agent):
        flash("Type agent mise à jour avec succès!", category='success')
        return render_template('type_agents/edit_type_agent.html', read_type_agent=read_type_agent)
    flash("Quelque chose s'est mal passé lors de la mise à jour du type agent !", category='error')
    return render_template('type_agents/edit_type_agent.html', read_type_agent=read_type_agent)


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
    type_budget = request.form.get("type_budget")
    montant_budget_mission = request.values.get("montant_budget_mission")
    devise_budget = request.form.get("devise_budget")
    date_depart_mission = request.values.get("date_depart_mission")
    date_retour_mission = request.values.get("date_retour_mission")
    pays_destination_mission = request.form.getlist("pays_destination_mission")
    ville_pays_destination_mission = request.form.getlist("ville_pays_destination_mission")
    agents_mission = request.form.getlist("agents_mission")
    moyen_transport_mission = request.values.get("moyen_transport_mission")
    commune_mission = request.values.get("commune_mission")
    immatriculation_moyen_transport_mission = request.values.get("immatriculation_moyen_transport_mission")
    structure_initiatrice_mission = request.form.get("structure_initiatrice_mission")
    code_type_localite_mission = request.values.get("code_type_localite_mission")
    libelle_localite_mission = request.values.get("libelle_localite_mission")
    code_localite_parente_mission = request.values.get("code_localite_parente_mission")
    reference_lettre_de_mission = request.values.get("reference_lettre_de_mission")
    code_localite_mission = request.values.get("code_localite_mission")
    to_save_mission = {"date_debut_mission": dateutil.parser.parse(date_debut_mission),
                       "date_fin_mission": dateutil.parser.parse(date_fin_mission),
                       "responsable_structure": responsable_structure,
                       "reference_lettre_de_mission": reference_lettre_de_mission,
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
                       "date_retour_mission": dateutil.parser.parse(date_retour_mission),
                       "date_depart_mission": dateutil.parser.parse(date_depart_mission),
                       "devise_budget": devise_budget,
                       "montant_budget_mission": montant_budget_mission,
                       "objet_mission": objet_mission, "destination_mission": destination_mission,
                       "reference_ordre_mission": reference_ordre_mission,
                       "type_budget": type_budget,
                       "created_at": dateutil.parser.parse(str(datetime.now())),
                       "status_mission": "En attente de validation",
                       "auteur": "Hilaire"
                       }
    missi = mission.Mission()

    struc = structure.Structure()
    list_structures = struc.get_structures()

    for agt in agents_mission:

        if missi.chech_mission_for_agent_between_two_dates(agt, date_debut_mission, date_fin_mission):
            flash(
                "L'agent " + agt + " a déjà une mission en cours dans la période de " + date_debut_mission + " au " + date_fin_mission,
                category='error')
            return render_template('missions/missions.html', list_agents=list_agents, list_pays=list_pays,
                                   list_type_budget=list_type_budget, list_structures=list_structures)

    for agt in agents_mission:
        if missi.check_if_agent_has_already_on_mission_for_end_date(agt, date_debut_mission, date_fin_mission):
            flash(
                "L'agent " + agt + " a déjà une mission en cours dans la période de " + date_debut_mission + " au " + date_fin_mission,
                category='error')
            return render_template('missions/missions.html', list_agents=list_agents, list_pays=list_pays,
                                   list_type_budget=list_type_budget, list_structures=list_structures)

    if missi.create_new_mission(to_save_mission):
        flash("Mission créé avec succès!", category='success')
        return render_template('missions/missions.html', list_agents=list_agents, list_pays=list_pays,
                               list_type_budget=list_type_budget, list_structures=list_structures)
    flash("Quelque chose s'est mal passé lors de la création de la mission !", category='error')
    return render_template('missions/missions.html', list_agents=list_agents, list_pays=list_pays,
                           list_type_budget=list_type_budget, list_structures=list_structures)


@app.route('/update_mission/<id_mission>', methods=['GET', 'POST'])
def updat_missions(id_mission):
    read_mission = mission.Mission().get_mission(str(id_mission))
    agt = agent.Agent()
    list_agents = agt.get_agents()
    typ_budg = type_budgets.TypeBudget()
    list_type_budget = typ_budg.get_type_budgets()
    pay = pays.Pays()
    list_pays2 = pay.get_payss()

    if read_mission:
        return render_template('missions/edit_mission.html', read_mission=read_mission, list_agents=list_agents,
                               list_pays=list_pays2,
                               list_type_budget=list_type_budget)
    flash("Quelque chose s'est mal passé lors de la mise à jour de la mission !", category='error')
    return render_template('missions/list_mission.html', read_mission=read_mission, list_agents=list_agents,
                           list_pays=list_pays2,
                           list_type_budget=list_type_budget)


@app.route('/mission_update/<id_mission>', methods=['GET', 'POST'])
def save_updated_missions(id_mission):
    agt = agent.Agent()
    list_agents = agt.get_agents()
    typ_budg = type_budgets.TypeBudget()
    list_type_budget = typ_budg.get_type_budgets()
    pay = pays.Pays()
    list_pays = pay.get_payss()

    date_debut_mission = request.values.get("date_debut_mission")
    date_fin_mission = request.values.get("date_fin_mission")
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
                         "type_budget": type_budget,
                         "updated_at": datetime.now(),
                         "montant_budget_mission": montant_budget_mission,
                         "objet_mission": objet_mission, "destination_mission": destination_mission,
                         "reference_ordre_mission": reference_ordre_mission}
    missi = mission.Mission()
    if missi.update_mission(id_mission, to_update_mission):
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
    list_cities_of_each_country = ville.Ville().get_all_cities_for_countries(list_countries)

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
        return render_template('corps/corps.html', message="ok")
    flash("Ce libelle du type agent a été déjà utilisé !", category='error')
    return render_template('corps/corps.html', message="ko")


@app.route('/corps_update/<id_corps>', methods=['GET', 'POST'])
def save_corps_updated(id_corps):
    corps1 = corps.Corps()
    read_corps = corps1.get_corps(str(id_corps))

    libelle_corps = request.values.get("libelle_corps")
    crps = {"libelle_corps": libelle_corps
        , "last_updated_at": datetime.now()}
    crps1 = corps.Corps()

    if libelle_corps is not None:
        if crps1.update_corps(id_corps, crps):
            flash("Corps mise à jour avec succès!", category='success')
            return render_template('corps/edit_corps.html', read_corps=read_corps)
        flash("Ce libelle du type agent a été déjà utilisé !", category='error')
        return render_template('corps/edit_corps.html', read_corps=read_corps)
    return render_template('corps/edit_corps.html', read_corps=read_corps)


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


@app.route('/grade_update/<id_grade>', methods=['GET', 'POST'])
def save_grade_updated(id_grade):
    grade1 = grade.Grade()
    read_grade = grade1.get_grade(str(id_grade))

    libelle_grade = request.values.get("libelle_grade")

    grad = {"libelle_grade": libelle_grade
        , "last_updated_at": datetime.now()}
    grad1 = grade.Grade()
    if list_grade is not None:
        if grad1.update_grade(id_grade, grad):
            flash("Grade mise à jour avec succès!", category='success')
            return render_template('grades/edit_grade.html', read_grade=read_grade)
        flash("Oups , quelque chose s'est mal passé lors de la mise à jour du grade !", category='error')
        return render_template('grades/edit_grade.html', read_grade=read_grade)

    return render_template('grades/edit_grade.html', read_grade=read_grade)


@app.route('/mission/<id_mission>')
def read_mission_by_id(id_mission):
    miss = mission.Mission()
    read_mission = miss.get_mission(str(id_mission))
    return render_template('missions/show_mission.html', read_mission=read_mission)


@app.route('/validate_mission/<id_mission>')
def validate_mission(id_mission):
    miss1 = mission.Mission()
    list_missions = miss1.get_missions()
    if mission.Mission().validate_mission(id_mission):
        flash("Mission vaildée avec succès!", category='success')
        return render_template('missions/list_mission.html', list_missions=list_missions)
    flash("Quelque chose s'est mal passé lors de la validation de la mission !", category='error')
    return render_template('missions/list_mission.html', list_missions=list_missions)


@app.route('/delete_mission/<id_mission>')
def delete_mission(id_mission):
    miss1 = mission.Mission()
    list_missions = miss1.get_missions()
    if mission.Mission().delete_mission(str(id_mission)):
        flash("Mission supprimée avec succès!", category='success')
        return render_template('missions/list_mission.html', list_missions=list_missions)
    flash("Quelque chose s'est mal passé lors de la suppression de la mission !", category='error')
    return render_template('missions/list_mission.html', list_missions=list_missions)


@app.route('/delete_qualite/<id_qualite>')
def delete_qualite(id_qualite):
    qual1 = qualite.Qualite()

    list_qualites = qual1.get_qualites()
    if qual1.delete_qualite(str(id_qualite)):
        flash("Qualité supprimée avec succès!", category='success')
        return render_template('qualites/list_qualite.html', list_qualites=list_qualites)
    flash("Quelque chose s'est mal passé lors de la suppression de la qualité !", category='error')
    return render_template('quailites/list_qualite.html', list_qualites=list_qualites)


@app.route('/delete_corps/<id_corps>')
def delete_corps(id_corps):
    corps1 = corps.Corps()
    list_corps = corps1.get_corpss()
    if corps1.delete_corps(str(id_corps)):
        flash("Corps supprimé avec succès!", category='success')
        return render_template('corps/list_corps.html', list_corps=list_corps)
    flash("Quelque chose s'est mal passé lors de la suppression du corps !", category='error')
    return render_template('corps/list_corps.html', list_corps=list_corps)


@app.route('/delete_grade/<id_grade>')
def delete_grade(id_grade):
    grade1 = grade.Grade()
    list_grade2 = grade1.get_grades()
    if grade1.delete_grade(str(id_grade)):
        flash("Grade supprimé avec succès!", category='success')
        return render_template('grades/list_grade.html', list_grades=list_grade2)
    flash("Quelque chose s'est mal passé lors de la suppression du grade !", category='error')
    return render_template('grades/list_grade.html', list_grades=list_grade2)


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


@app.route("/ordre_de_mission/<id_mission>")
def ordre_de_mission(id_mission):
    structu = structure.Structure()
    mis = mission.Mission().get_mission(id_mission)
    read_struc = structu.get_structure_by_code(str(mis['structure_initiatrice_mission']))

    list_agts = mis['agents_mission']
    list_agents = []
    for agt in list_agts:
        agent_x = agent.Agent().get_agent_by_ifu(str(agt).split()[0])
        list_agents.append(agent_x)
    return render_template('missions/odm.html', mission=mis, list_agents=list_agents, current_time=datetime.now(),
                           read_struc=read_struc)


def groupe_ville_by_pay():
    list_pays = pays.Pays().get_payss()
    list_villes = ville.Ville().get_villes()
    list_pays_to_return = []
    list_ville_to_return = []
    for pays in list_pays:
        for ville in list_villes:
            if str(pays['libelle_fr_pays']).lower() == str(ville['libelle_fr_pays']).lower():
                list_ville_to_return.append(ville['non_ville'])
        list_pays_to_return['pays'] = pays['libelle_fr_pays']
        list_pays_to_return.append(list_ville_to_return)
    return list_pays_to_return


@app.route('/login2', methods=['GET', 'POST'])
def login2():
    form = LoginForm()
    if request.method == 'POST':
        user1 = app.config['USERS_COLLECTION'].find_one({"_id": form.username.data})

        if user1 and User.validate_login(user1['password'], form.password.data):
            user_obj = User(user1['_id'])
            login_user(user_obj)
            flash("Logged in successfully!", category='success')
            return redirect(request.args.get("next") or url_for("write"))
        flash("Wrong username or password!", category='error')
    return render_template('login.html', title='login', form=form)
