import logging
import _config as conf
from flask import Flask
from controller import routes
import pyldapi

app = Flask(__name__, template_folder=conf.TEMPLATES_DIR, static_folder=conf.STATIC_DIR)
app.register_blueprint(routes.routes)


# run the Flask app
if __name__ == '__main__':
    logging.basicConfig(filename=conf.LOGFILE,
                        level=logging.DEBUG,
                        datefmt='%Y-%m-%d %H:%M:%S',
                        format='%(asctime)s %(levelname)s %(filename)s:%(lineno)s %(message)s')

    # generate the RDF sitemap
    ''''
        * call each Rule's endpoint
            * if it returns a reg view
                * read that for a local superregister property
                    * add knowledge to graph for file storage
            * else 
                * it must be the R of R
    
    '''


    thread = pyldapi.setup(app, conf.URI_BASE)

    app.run(debug=conf.DEBUG, use_reloader=False)

    thread.join()