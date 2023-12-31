from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import re
from config import database_url, content_article_table, branding_info_table

app = Flask(__name__, static_folder="static", static_url_path="/static")
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
db = SQLAlchemy(app)


class ContentArticleDB(db.Model):
    __tablename__ = content_article_table

    id = db.Column(db.Integer, primary_key=True, index=True)
    request_id = db.Column(db.String)
    created_date = db.Column(db.Date)
    article = db.Column(db.String)
    article_markup = db.Column(db.String)
    summary = db.Column(db.String)
    headline = db.Column(db.String)
    slug = db.Column(db.String)
    category_tags = db.Column(db.String)
    primary_tag = db.Column(db.String)
    fb_post = db.Column(db.String)
    reviewed = db.Column(db.Boolean)
    reviewed_date = db.Column(db.Date)
    img_url_1 = db.Column(db.String)
    img_url_2 = db.Column(db.String)
    img_url_3 = db.Column(db.String)
    img_url_4 = db.Column(db.String)
    img_url_5 = db.Column(db.String)
    published = db.Column(db.Boolean)
    published_date = db.Column(db.Date)
    published_site = db.Column(db.String)
    word_count = db.Column(db.Integer)
    read_time = db.Column(db.Integer)
    source_url = db.Column(db.String)
    featured = db.Column(db.Boolean)
    recommended = db.Column(db.Boolean)
    primary_tag_slug = db.Column(db.String)


class BrandingData(db.Model):
    __tablename__ = branding_info_table

    id = db.Column(db.Integer, primary_key=True, index=True)
    brand_title = db.Column(db.String)
    brand_description = db.Column(db.Text)
    brand_disclaimer_1 = db.Column(db.Text)
    brand_disclaimer_2 = db.Column(db.Text)
    brand_terms_name_and_address = db.Column(db.String)
    brand_contact_email = db.Column(db.String)
    brand_website = db.Column(db.String)
    primary_theme_color = db.Column(db.String)
    secondary_theme_color = db.Column(db.String)
    logo_url = db.Column(db.String)
    favicon_url = db.Column(db.String)
    brand_disclaimer_3 = db.Column(db.Text)
    social_url_fb = db.Column(db.String)
    social_url_twitter = db.Column(db.String)
    social_url_youtube = db.Column(db.String)
    social_url_instagram = db.Column(db.String)
    social_url_pinterest = db.Column(db.String)
    social_active_fb = db.Column(db.Boolean)
    social_active_twitter = db.Column(db.Boolean)
    social_active_youtube = db.Column(db.Boolean)
    social_active_instagram = db.Column(db.Boolean)
    social_active_pinterest = db.Column(db.Boolean)

def get_site_theme():
    # Retrieve the single record from the BrandingData table
    branding_record = BrandingData.query.first()

    # Access the primary_theme_color and secondary_theme_color attributes
    primary_theme_color = branding_record.primary_theme_color
    secondary_theme_color = branding_record.secondary_theme_color

    # primary_theme_color = "#FF0000"
    # secondary_theme_color = "#FF00FF"

    theme_context = {
        'primary_theme_color': primary_theme_color,
        'secondary_theme_color': secondary_theme_color,
    }

    return theme_context


def get_branding_data():
    # Retrieve the single record from the BrandingData table
    branding_record = BrandingData.query.first()

    if branding_record is None:
        return None  # or handle this case differently, as appropriate for your application

    # Package the data in the desired format
    branding_data = {
        "brand_title": branding_record.brand_title,
        "brand_description": branding_record.brand_description,
        "brand_disclaimer_1": branding_record.brand_disclaimer_1,
        "brand_disclaimer_2": branding_record.brand_disclaimer_2,
        "brand_terms_name_and_address": branding_record.brand_terms_name_and_address,
        "brand_contact_email": branding_record.brand_contact_email,
        "brand_website": branding_record.brand_website,
        "primary_theme_color": branding_record.primary_theme_color,
        "secondary_theme_color": branding_record.secondary_theme_color,
        "logo_url": branding_record.logo_url,
        "social_url_fb": branding_record.social_url_fb,
        "social_url_twitter": branding_record.social_url_twitter,
        "social_url_youtube": branding_record.social_url_youtube,
        "social_url_instagram": branding_record.social_url_instagram,
        "social_url_pinterest": branding_record.social_url_pinterest,
        "social_active_fb": branding_record.social_active_fb,
        "social_active_twitter": branding_record.social_active_twitter,
        "social_active_youtube": branding_record.social_active_youtube,
        "social_active_instagram": branding_record.social_active_instagram,
        "social_active_pinterest": branding_record.social_active_pinterest,
    }

    return branding_data


def filter_published(results, published=True):
    return [item for item in results if item.published == published]



def get_core_context():
    recent_articles = ContentArticleDB.query.order_by(ContentArticleDB.id.desc()).limit(20).all()
    featured_articles = ContentArticleDB.query.filter(ContentArticleDB.featured == True).limit(20).all()
    recommended_articles = ContentArticleDB.query.filter(ContentArticleDB.recommended == True).limit(20).all()
    recent_articles = filter_published(recent_articles)
    featured_articles = filter_published(featured_articles)
    recommended_articles = filter_published(recommended_articles)

    branding_data = get_branding_data()

    core_context = {

        "recent_articles": recent_articles,
        "featured_articles": featured_articles,
        "recommended_articles": recommended_articles,
        "branding_data": branding_data,
        'year': datetime.utcnow().strftime('%Y')
    }
    ########## ADD IN THE SITE THEME TO THE CONTEXT ################
    core_context.update(get_site_theme())
    core_context.update(get_topics())

    return core_context


def slugify(s):
    """
    Simplifies ugly strings into something URL-friendly.
    """
    # "[^\w\s-]" removes unwanted characters.
    s = re.sub(r'[^\w\s-]', '', s)
    # "\s+" changes any whitespace (like \n, \r, \t, \v, \f) into one dash "-".
    s = re.sub(r'\s+', '-', s)
    # "^-" removes any dashes "-" at the start of the string.
    s = re.sub(r'^-', '', s)
    # "-$" removes any dashes "-" at the end of the string.
    s = re.sub(r'-$', '', s)
    # "^\s+|\s+$" removes any whitespace at the start or end.
    s = re.sub(r'^\s+|\s+$', '', s)
    # Everything is lowercased.
    s = s.lower()

    return s

def get_topics():
    unique_tags = ContentArticleDB.query.with_entities(ContentArticleDB.primary_tag.distinct()).all()
    topic_list = [tag[0] for tag in unique_tags if tag[0] is not None]
    topic_dict = {slugify(topic): topic for topic in topic_list}

    return {"topic_dict": topic_dict}


def get_related_articles(primary_tag):
    related_articles = []
    all_related = ContentArticleDB.query.filter(ContentArticleDB.primary_tag == primary_tag).order_by(
        ContentArticleDB.id.desc()).all()

    all_related = filter_published(all_related)

    for related in all_related:
        if related.recommended == True:
            related_articles.append(related)
    if len(related_articles) < 3:
        for related in all_related:
            if related.featured == True:
                related_articles.append(related)
    if len(related_articles) < 3:
        for related in all_related[:3]:
            related_articles.append(related)

    return related_articles


@app.route("/", methods=["GET"])
def index():

    context = get_core_context()

    return render_template("index.html", **context)


@app.route("/article/<id>", methods=["GET"])
def blog_details(id):
    article = ContentArticleDB.query.filter(ContentArticleDB.id == id).first()
    primary_tag = article.primary_tag
    related_articles = get_related_articles(primary_tag)
    related_articles = [each for each in related_articles if each.id != article.id]

    context = {
        "article": article,
        "related_articles": related_articles,
        "no_related_flag": False
    }
    context.update(get_core_context())

    featured_articles = context['featured_articles']
    if len(related_articles) < 1:
        context['related_articles'] = featured_articles
        context['no_related_flag'] = True

    if article.published:
        return render_template("blog-details.html", id=id, **context)
    else:
        return {"Error": "The article ID does not exist or the article is not published"}



@app.route("/topic/<topic_slug>", methods=["GET"])
def blog_list_topic_view(topic_slug):
    topic_slug = topic_slug
    topics = get_topics()
    primary_tag = topics['topic_dict'][topic_slug]

    topic_articles = ContentArticleDB.query.filter(ContentArticleDB.primary_tag == primary_tag).all()
    topic_articles = filter_published(topic_articles)
    related_articles = get_related_articles(primary_tag)

    context = {
        "topic_articles": topic_articles,
        "related_articles": related_articles
    }
    context.update(get_core_context())

    return render_template("blog-list-topic.html", primary_tag=primary_tag, **context)


@app.route("/search/", methods=["GET"])
def blog_list_search_view():
    search_term = request.args.get('search_term')
    search_articles = {}
    search_articles_headline = ContentArticleDB.query.filter(ContentArticleDB.headline.contains(search_term)).all()
    search_articles = filter_published(search_articles)
    search_articles_summary = ContentArticleDB.query.filter(ContentArticleDB.summary.contains(search_term)).all()
    search_articles_summary = filter_published(search_articles_summary)
    if len(search_articles_headline) > 0:
        search_articles = search_articles_headline
    if len(search_articles_summary) > 0:
        if len(search_articles) > 0:
            search_articles.update(search_articles_summary)
        else:
            search_articles = search_articles_summary

    context = {
        "search_term": search_term,
        "search_articles": search_articles,

    }
    context.update(get_core_context())

    return render_template("blog-list-search-results.html", **context)


@app.route("/recent", methods=["GET"])
def blog_list_recent_view():
    context = get_core_context()

    return render_template("blog-list-recent.html", **context)


@app.route("/popular", methods=["GET"])
def blog_list_popular_view():
    context = get_core_context()

    return render_template("blog-list-recommended.html", **context)


@app.route("/privacy", methods=["GET"])
def privacy_policy_view():
    context = get_core_context()

    return render_template("privacy_policy.html", **context)


@app.route("/terms-and-conditions", methods=["GET"])
def terms_and_conditions_view():
    context = get_core_context()

    return render_template("terms_and_conditions.html", **context)


@app.route("/test/", methods=["GET"])
def test():
    context = get_core_context()

    return render_template("test.html", **context)


@app.errorhandler(404)
def page_not_found(error):
    context = get_core_context()

    return redirect(url_for('index'))



if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(host="127.0.0.1", port=8000, debug=True)
