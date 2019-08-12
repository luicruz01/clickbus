#!/usr/bin/python
from flask_restful import Api


class ExemptionApi(Api):
    def add_resource(self, resource, *urls, **kwargs):
        """Add resource making sure docs resources are exempt from limiter.

        add_resource() receives the name of a Resource class, instantiates
        it and then applies the decorators to each function of the instantiated
        resource. To be able to bypass the limiter, Swagger Resources' functions
        have to have the '@limiter.exempt' decorator.

        There are two ways to apply the decorators. The first is to mark the
        function as decorated, but since this is an external library that is not
        a viable option. The second one is to pass the decorator as an argument
        when creating the Api instance. However, this would apply the decorator
        to ALL resources added to the Api, defeating the purpose of the limiter.

        In order to bypass the limiter ONLY for Swagger Resources, ExemptionApi
        checks the Resource's module. If it is a Swagger Resource, it adds
        the required 'limiter.exempt' decorator to the class's decorators before
        calling the super's method and removes it afterwards.

        """
        temp_decorators = self.decorators[:]
        if resource.__module__ == 'flask_restful_swagger.swagger':
            self.decorators.append(self.limiter.exempt)
        super(ExemptionApi, self).add_resource(resource, *urls, **kwargs)
        self.decorators = temp_decorators

    def __init__(self, limiter, *args, **kwargs):
        self.exempt_resources = kwargs.pop('exempt_resources', [])
        super(ExemptionApi, self).__init__(*args, **kwargs)
        self.limiter = limiter
