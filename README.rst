Introduction
============

The "IReferenceable" behavior is used for enabling UUID (plone.app.uuid) support
for dexterity contents, like in archetypes content types. This allow for example
references between archetypes and dexterity content types.

Note: It can't work with Plone==4.0 because it is based on plone.uuid integration in
CMF. It is compatible with Plone>=4.1

Usage
-----

Just use the behavior "plone.app.referenceablebehavior.referenceable.IReferenceable" in
your dexterity content type.

In your *profiles/default/types/YOURTYPE.xml* add the behavior::

    <?xml version="1.0"?>
    <object name="example.conference.presenter" meta_type="Dexterity FTI"
       i18n:domain="example.conference" xmlns:i18n="http://xml.zope.org/namespaces/i18n">

     <!-- enabled behaviors -->
     <property name="behaviors">
         <element value="plone.app.referenceablebehavior.referenceable.IReferenceable" />
     </property>

    </object>
