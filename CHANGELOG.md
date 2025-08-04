# Changelog

## [0.50.2](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.50.1...v0.50.2) (2025-08-04)


### Bug Fixes

* **collections:** rename view attribute to `obj_content_type` ([64fcca8](https://github.com/acdh-oeaw/apis-core-rdf/commit/64fcca8bb30e0fb54a7f6878933ec1cc1d4bdbce))
* **generic:** also add/remove collections if they are an empty list ([775bb59](https://github.com/acdh-oeaw/apis-core-rdf/commit/775bb59a45bffdad0c2567f8e900f2bd6764f0dd))
* **history:** run flattening on m2m fields only ([79fb332](https://github.com/acdh-oeaw/apis-core-rdf/commit/79fb332e25186aead636fe282cf98dcfed4adc8a))

## [0.50.1](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.50.0...v0.50.1) (2025-07-31)


### Bug Fixes

* **collections:** check for filter existence before removing ([0bc979e](https://github.com/acdh-oeaw/apis-core-rdf/commit/0bc979ec659dae52f95f1c019699753687039ede)), closes [#1978](https://github.com/acdh-oeaw/apis-core-rdf/issues/1978)
* **relations:** make subj & obj check in Relation.save less strict ([b687a4e](https://github.com/acdh-oeaw/apis-core-rdf/commit/b687a4e04cc6a93d9cd3440a883690f4b8404ffc)), closes [#1896](https://github.com/acdh-oeaw/apis-core-rdf/issues/1896)
* **relations:** remove collections filter from relations filterset ([13a9b59](https://github.com/acdh-oeaw/apis-core-rdf/commit/13a9b5974aed506b403f1c391c567c8ea5e10443)), closes [#1970](https://github.com/acdh-oeaw/apis-core-rdf/issues/1970)

## [0.50.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.49.1...v0.50.0) (2025-07-29)


### ⚠ BREAKING CHANGES

* **generic:** We replace the `generic/partials/object_card.html` with `apis_core/generic/genericmodel_card.html`. Please adapt your templates accordingly.

### Features

* **apis_entities:** add absolute url link next to object title ([80c535e](https://github.com/acdh-oeaw/apis-core-rdf/commit/80c535e3b9729058a9a929496a1f85a15ea55711))
* **apis_entities:** only show external URIs in LOD section ([815ec76](https://github.com/acdh-oeaw/apis-core-rdf/commit/815ec76e28ce59b14e34f94d986a79106ed05f3a))
* **collections:** add custom filterset for SkosCollectionContentObject ([2be3eb5](https://github.com/acdh-oeaw/apis-core-rdf/commit/2be3eb5cc7647e8033b979fbf46d699d4270957a))
* **collections:** change menu to link also to list of linked objects ([178e476](https://github.com/acdh-oeaw/apis-core-rdf/commit/178e47614b1a58c1dbf95cef2be3db674c0f9ca1))
* **collections:** only show collection menu if permission exist ([081c8ba](https://github.com/acdh-oeaw/apis-core-rdf/commit/081c8ba7f84a7cfae3deb287f716b054c70f0e80)), closes [#1924](https://github.com/acdh-oeaw/apis-core-rdf/issues/1924)
* **core:** add password-change link to user menu ([ceb784b](https://github.com/acdh-oeaw/apis-core-rdf/commit/ceb784b78da3b64771ebe331ee59c6d87fc142a6))
* **core:** introduce a `password-change` interface ([6038fed](https://github.com/acdh-oeaw/apis-core-rdf/commit/6038feddca919ee645f3def9fbae79e506e6f38d))
* **generic:** add options to mro_paths ([0845664](https://github.com/acdh-oeaw/apis-core-rdf/commit/08456646c77c0171bf4bc9e0502957b8e0085f9a))
* **generic:** make ModelImportChoiceField more robust ([e4b747d](https://github.com/acdh-oeaw/apis-core-rdf/commit/e4b747dea14d1cabc16c5355a09c71b56177b679))
* **generic:** use `template_list` templatetag in `generic_detail.html` ([9098e19](https://github.com/acdh-oeaw/apis-core-rdf/commit/9098e19ce6b1c5a032fb03fc987563f588420250))
* **generic:** use custom properties for the action colors ([44905bc](https://github.com/acdh-oeaw/apis-core-rdf/commit/44905bc44fdc91ff437f1f279bb1cb4201ddb7a6)), closes [#1953](https://github.com/acdh-oeaw/apis-core-rdf/issues/1953)
* **relations:** introduce a `relation_card_table.html` template ([e093d86](https://github.com/acdh-oeaw/apis-core-rdf/commit/e093d86ae942967d8c8871996d54582d29fdafdc))
* **relations:** introduce a `relation_card.html` template ([b6cb9d3](https://github.com/acdh-oeaw/apis-core-rdf/commit/b6cb9d38fc370e236cb8a613b85470fbf5cd4745)), closes [#1728](https://github.com/acdh-oeaw/apis-core-rdf/issues/1728)
* **relations:** introduce indexes for the relation model ([3942587](https://github.com/acdh-oeaw/apis-core-rdf/commit/3942587a5d92747e32075e31a0cdfc0555742e7f)), closes [#1952](https://github.com/acdh-oeaw/apis-core-rdf/issues/1952)
* **relations:** refactor the whole relations form ([8ef00b1](https://github.com/acdh-oeaw/apis-core-rdf/commit/8ef00b1d75fc2871b217984b5829775aa7835ee5))


### Bug Fixes

* **apis_entities:** link to absolute url in local autocomplete results ([6de589f](https://github.com/acdh-oeaw/apis-core-rdf/commit/6de589fd002a4b394cb9ff2350e5054cbdec13e0))
* **generic:** add label to collection form field ([0ab326e](https://github.com/acdh-oeaw/apis-core-rdf/commit/0ab326eebb9dcda4a459f6b826af95faf8f741e6))
* **relations:** adapt template translation to include object ([2957cc3](https://github.com/acdh-oeaw/apis-core-rdf/commit/2957cc35300047219bfbcde4cda88f15ebb9314b))


### Documentation

* **readme:** correct link to creating your ontology ([eca13fd](https://github.com/acdh-oeaw/apis-core-rdf/commit/eca13fd7ec8befd11af2df09df939b009b25f23c))

## [0.49.1](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.49.0...v0.49.1) (2025-06-25)


### Bug Fixes

* **generic:** use the cleaned url from importer when enriching ([c166406](https://github.com/acdh-oeaw/apis-core-rdf/commit/c166406d8ea6bc8c0c0352250fabc6196989ff90))
* **relations:** use `.pk` instead of `.id` ([11af495](https://github.com/acdh-oeaw/apis-core-rdf/commit/11af495b2dd83de0eea4ec8764c70fde4b8b52a6))

## [0.49.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.48.2...v0.49.0) (2025-06-23)


### Features

* **history:** flatten many-to-many relations in ModelChanges ([f58e371](https://github.com/acdh-oeaw/apis-core-rdf/commit/f58e3717a5f2568b7a0f98661f3f4f8285cc39e0))
* **history:** set the `foreign_keys_are_objs` argument to True ([b077fc2](https://github.com/acdh-oeaw/apis-core-rdf/commit/b077fc2b83782fc4cba8e74c4746874c78db52f8))
* **relations:** allow subj_object_id and obj_object_id to be null ([8ae4335](https://github.com/acdh-oeaw/apis-core-rdf/commit/8ae4335ec5228fceb56cf3970be97050250d5660))
* **relations:** implement signal to nullify relation ids ([4ca4c41](https://github.com/acdh-oeaw/apis-core-rdf/commit/4ca4c41802ea2b26b15bf33a98e87e6b766661ea))
* **relations:** update template to reflect targets that are None ([81d0a8c](https://github.com/acdh-oeaw/apis-core-rdf/commit/81d0a8c9323224a0adb899f20fee01706be99529))
* **relations:** warn user when obj_model or subj_model are lists ([765a5a1](https://github.com/acdh-oeaw/apis-core-rdf/commit/765a5a1e65edc6338f3e13bb94ccbba9e84f0dd3)), closes [#1923](https://github.com/acdh-oeaw/apis-core-rdf/issues/1923)
* **sample_project:** add versionperson_profession entries to fixtures ([be56610](https://github.com/acdh-oeaw/apis-core-rdf/commit/be566103fa23c1992de64227694bb7911aeba61f))
* **sample_project:** use VersionMixin on Profession ([cf6c991](https://github.com/acdh-oeaw/apis-core-rdf/commit/cf6c9917631ae2773c5616f77e8006c359996274))


### Bug Fixes

* **core:** drop `modal` block ([efc2c82](https://github.com/acdh-oeaw/apis-core-rdf/commit/efc2c82acf23ba4b3e22e730552c12b27df51a69)), closes [#1917](https://github.com/acdh-oeaw/apis-core-rdf/issues/1917)
* **generic:** catch exception if relation could not be imported ([737f328](https://github.com/acdh-oeaw/apis-core-rdf/commit/737f328ea5952335fae627013e1a79a24c56e91a))
* **generic:** only run importer if there is something to import from ([0b5b477](https://github.com/acdh-oeaw/apis-core-rdf/commit/0b5b4772e050ab274ccc48f83fb1d87bef519381))
* **relations:** adapt relation form for targets that are None ([22a6966](https://github.com/acdh-oeaw/apis-core-rdf/commit/22a69667a8f20153396aaaeab217d9d0cbd09ce0))
* **relations:** make relation field editable again ([7ed19c9](https://github.com/acdh-oeaw/apis-core-rdf/commit/7ed19c9ae44993c3b66e794e52a3922aa7f4722a)), closes [#1922](https://github.com/acdh-oeaw/apis-core-rdf/issues/1922)
* **sample_project:** add `feature_code` to place entities ([c3a78ef](https://github.com/acdh-oeaw/apis-core-rdf/commit/c3a78efa9942c2dee028c800371111dd332d67e6))

## [0.48.2](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.48.1...v0.48.2) (2025-06-18)


### Bug Fixes

* **core:** update alert close button to bootstrap 5 syntax ([17aa9a0](https://github.com/acdh-oeaw/apis-core-rdf/commit/17aa9a06fe7db180ca2c87cb026837aa7af520f8))
* **generic:** use first element of list for enriching entities ([3e50265](https://github.com/acdh-oeaw/apis-core-rdf/commit/3e502653d018b2805970928ffcdd8a09cb56fb7c))

## [0.48.1](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.48.0...v0.48.1) (2025-06-17)


### Bug Fixes

* **documentation:** revert inadvertently translated material symbol ([c255957](https://github.com/acdh-oeaw/apis-core-rdf/commit/c25595718ed599fd4a5dcf339276c3605f327d16)), closes [#1921](https://github.com/acdh-oeaw/apis-core-rdf/issues/1921)
* **generic:** use correct permission name for duplicate & merge ([304cd9e](https://github.com/acdh-oeaw/apis-core-rdf/commit/304cd9e60db7eb09f82c915f4a6ea0b0f62c77bd))
* **history:** revert "feat(history): use history queryset for views" ([8619ab3](https://github.com/acdh-oeaw/apis-core-rdf/commit/8619ab3997c246182fe9ef7bad570065ec807b48)), closes [#1919](https://github.com/acdh-oeaw/apis-core-rdf/issues/1919)

## [0.48.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.47.1...v0.48.0) (2025-06-04)


### Features

* **apis_entities:** add `create_from_string` methods ([b013ac4](https://github.com/acdh-oeaw/apis-core-rdf/commit/b013ac4b213aff0b7529d6cfd1216963b81e9c38)), closes [#1872](https://github.com/acdh-oeaw/apis-core-rdf/issues/1872)
* **apis_entities:** update rdf_configs for regex based matching ([32eaed1](https://github.com/acdh-oeaw/apis-core-rdf/commit/32eaed121acba7322896781718a4aa61375bd82a)), closes [#1257](https://github.com/acdh-oeaw/apis-core-rdf/issues/1257)
* **apis_entities:** use `get_verbose_name_plural` method instead filter ([31f4861](https://github.com/acdh-oeaw/apis-core-rdf/commit/31f4861af4960545e1248c3eab3ee5fef0c7c7e9))
* **deps:** replace `requests` with `httpx` ([278b87e](https://github.com/acdh-oeaw/apis-core-rdf/commit/278b87e12d2ddbc4529caecc293a6960629c7d27)), closes [#1040](https://github.com/acdh-oeaw/apis-core-rdf/issues/1040)
* **generic:** add `get_verbose_name_plural` method to GenericModel ([f264a97](https://github.com/acdh-oeaw/apis-core-rdf/commit/f264a97c5ebb282fb749d5f59bc3384f244aa7a3))
* **generic:** only show columns selector if there are columns to select ([d076708](https://github.com/acdh-oeaw/apis-core-rdf/commit/d0767082bfc577f1aa7023deaade1960cb60f49d))
* **generic:** use `get_verbose_name_plural` method instead of filter ([52aaefc](https://github.com/acdh-oeaw/apis-core-rdf/commit/52aaefce6dbfdf613ec814fceb2e23ac3339d656))
* **history:** add `get_reset_url` helper method to history models ([27dcdf0](https://github.com/acdh-oeaw/apis-core-rdf/commit/27dcdf01a9138a5c4f1f81a545f264083b47f4af))
* **history:** add a link to the reset view to the history table ([4550876](https://github.com/acdh-oeaw/apis-core-rdf/commit/455087673b389661dd525ee42abae56764f6109e))
* **history:** introduce view to reset object to a history version ([5097096](https://github.com/acdh-oeaw/apis-core-rdf/commit/5097096c335420f3ff6f2bccee3f6f7f83f4b33c)), closes [#283](https://github.com/acdh-oeaw/apis-core-rdf/issues/283)
* **history:** use history queryset for views ([ae5fecd](https://github.com/acdh-oeaw/apis-core-rdf/commit/ae5fecd44b71d1971e62ce31ee46ea46ae6fa31f))
* **sample_project:** compile translations on startup ([c30d185](https://github.com/acdh-oeaw/apis-core-rdf/commit/c30d185bb4a2ca29b0d909bdca25445816d8d52b))
* **utils:** refactor rdf config to use regex for uri matching ([ab7813f](https://github.com/acdh-oeaw/apis-core-rdf/commit/ab7813f423d09a9096e7618bc0909cf226cb818e))


### Bug Fixes

* **apis_entities:** drop `tag version` link from entity actions ([c9cfcab](https://github.com/acdh-oeaw/apis-core-rdf/commit/c9cfcaba1551962d1c8ccf26c04cda67f61f7e4f))
* **apis_entities:** reorder label & select place label using languages ([5101da1](https://github.com/acdh-oeaw/apis-core-rdf/commit/5101da1a7168894f28f216bb870d1318b5b7f03a)), closes [#1863](https://github.com/acdh-oeaw/apis-core-rdf/issues/1863)
* **apis_entities:** reorder name sources and also use variantName ([c76f8a1](https://github.com/acdh-oeaw/apis-core-rdf/commit/c76f8a1b668c8474688070013c6d846274d89c01)), closes [#1903](https://github.com/acdh-oeaw/apis-core-rdf/issues/1903)
* **generic:** catch ObjectDoesNotExist for remote fields ([d8ffaed](https://github.com/acdh-oeaw/apis-core-rdf/commit/d8ffaedb364237fc72b3f0291e71d05b9b3b3d93))
* **generic:** fix typo in rdf APPELLATION namespace ([e729ee0](https://github.com/acdh-oeaw/apis-core-rdf/commit/e729ee0a504ab61fec67f27205ba88251f620199))
* **generic:** replace slashes with underscores in ATTRIBUTES ids ([4439b6d](https://github.com/acdh-oeaw/apis-core-rdf/commit/4439b6d0a0de0ec4c5296d18b9b223eca10a973d)), closes [#1876](https://github.com/acdh-oeaw/apis-core-rdf/issues/1876)
* **generic:** use plural form in result header ([089dce1](https://github.com/acdh-oeaw/apis-core-rdf/commit/089dce101d2c4f421fd493cf7005dcc11e300515)), closes [#1874](https://github.com/acdh-oeaw/apis-core-rdf/issues/1874)
* **utils:** when resolving, also handle boolean `True` value ([05f6a6b](https://github.com/acdh-oeaw/apis-core-rdf/commit/05f6a6b9746b23b5fb3c46b7c147e8d4d8527ba9)), closes [#1905](https://github.com/acdh-oeaw/apis-core-rdf/issues/1905)

## [0.47.1](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.47.0...v0.47.1) (2025-05-19)


### Bug Fixes

* **generic:** only include title block once ([25f525b](https://github.com/acdh-oeaw/apis-core-rdf/commit/25f525b2d2e377e496b12e42987c4eb258c49230))

## [0.47.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.46.1...v0.47.0) (2025-05-16)


### Features

* **apis_entities:** drop override that is now handled in generic ([4c978e3](https://github.com/acdh-oeaw/apis-core-rdf/commit/4c978e3ad7bdf3608ac6113dc885cf8431b67a04))
* **apis_entities:** return rdf types for various base classes ([9b84773](https://github.com/acdh-oeaw/apis-core-rdf/commit/9b8477357a8200bb351f57e469d8c39ed04a4422))
* **generic:** add a title string to all the generic templates ([046a63d](https://github.com/acdh-oeaw/apis-core-rdf/commit/046a63db0ccf7e8be89e50a869c30295ea4d3d4b))
* **generic:** add skeleton method for returning rdf types ([f0d82c0](https://github.com/acdh-oeaw/apis-core-rdf/commit/f0d82c065f87f0fda68bf94b58aff4861927bafc))
* **generic:** replace download list with a dropdown ([d622892](https://github.com/acdh-oeaw/apis-core-rdf/commit/d6228922d62df4c59e4f506b0b0d8e158257f90f))
* **generic:** use instance rdf type list in generic cidoc serializer ([cd69425](https://github.com/acdh-oeaw/apis-core-rdf/commit/cd6942547a9013cf5d0e4b5950b74591e6cc1ee1))
* **sample_project:** add LocaleMiddleware to the list of middlewares ([6e1de25](https://github.com/acdh-oeaw/apis-core-rdf/commit/6e1de2501e9cdbff23876befacd1c53793bf2de1)), closes [#1867](https://github.com/acdh-oeaw/apis-core-rdf/issues/1867)


### Bug Fixes

* **apis_entities:** use implizit one-off serializer for GetEntityGeneric ([3ccace8](https://github.com/acdh-oeaw/apis-core-rdf/commit/3ccace820af1b0f84a663e9dacf42101643c62c8))
* **collections:** add missing translations for collections ([232e7ab](https://github.com/acdh-oeaw/apis-core-rdf/commit/232e7abd335271aea8ff73e5a4fa16e23ae2e353)), closes [#1857](https://github.com/acdh-oeaw/apis-core-rdf/issues/1857)


### Documentation

* fix grammar, spelling, punctuation ([2680e8f](https://github.com/acdh-oeaw/apis-core-rdf/commit/2680e8f417d922cd0d7fccdf342421fdda8b2d2c)), closes [#1752](https://github.com/acdh-oeaw/apis-core-rdf/issues/1752)

## [0.46.1](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.46.0...v0.46.1) (2025-05-14)


### Bug Fixes

* **sample_project:** remove `version_tag` attribute from fixtures ([7656a59](https://github.com/acdh-oeaw/apis-core-rdf/commit/7656a5980f419a1ce45ca4bf7816ccb14d96909c))

## [0.46.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.45.1...v0.46.0) (2025-05-12)


### Features

* **apis_entities:** add default title for abstractentity template ([78f775d](https://github.com/acdh-oeaw/apis-core-rdf/commit/78f775d4d8af6f2fc54be9dd92f349b97451a219))
* **apis_entities:** introduce E53_PlaceCidocSerializer ([68f68be](https://github.com/acdh-oeaw/apis-core-rdf/commit/68f68bec7ff9893fbd2fd3b17b5448abf3735725))
* **apis_entities:** introduce E74_GroupCidocSerializer ([226aff9](https://github.com/acdh-oeaw/apis-core-rdf/commit/226aff988d6c32ccb3805de166768cbb777c5bb8))
* **core:** replace hardcoded bootstrap class with custom values ([c6e0b55](https://github.com/acdh-oeaw/apis-core-rdf/commit/c6e0b558722c9b268994e8977b24b87c0f457390)), closes [#1855](https://github.com/acdh-oeaw/apis-core-rdf/issues/1855)
* **generic:** add `action` argument to serializer factory ([5fe6080](https://github.com/acdh-oeaw/apis-core-rdf/commit/5fe60809ff16ddfddc51da3a1e40365fc9822949))
* **generic:** add default titles for detail and list templates ([0743ebd](https://github.com/acdh-oeaw/apis-core-rdf/commit/0743ebded0ce96e5093b885145225fef51b32f91))
* **generic:** pass the action name to the serializer factory ([b7a356a](https://github.com/acdh-oeaw/apis-core-rdf/commit/b7a356a2f3de058a2cce2f19921e93c6e80918f0))
* **history:** drop history version_tag field ([80f5398](https://github.com/acdh-oeaw/apis-core-rdf/commit/80f5398b8f55a50d29a5756c08ac4b5544016a81)), closes [#1843](https://github.com/acdh-oeaw/apis-core-rdf/issues/1843)


### Bug Fixes

* **apis_metainfo:** move method from utils to apis_metainfo.utils ([f7869f7](https://github.com/acdh-oeaw/apis-core-rdf/commit/f7869f7669c9e3d665984dee28323fcfd08e9ac9)), closes [#1816](https://github.com/acdh-oeaw/apis-core-rdf/issues/1816)
* **collections:** filter by pk and not by id ([baa0da4](https://github.com/acdh-oeaw/apis-core-rdf/commit/baa0da4284791bfde3ee9672ec196540875711a8))
* **collections:** use `.pk` instead of `.id` for collection mgmt ([c3c7654](https://github.com/acdh-oeaw/apis-core-rdf/commit/c3c76541b006d7d091225c20e68fd0e8613a4544))
* **core:** drop the fallback for the title block ([12bcc38](https://github.com/acdh-oeaw/apis-core-rdf/commit/12bcc3807ec54609fda71250320c041b86e46e51)), closes [#1769](https://github.com/acdh-oeaw/apis-core-rdf/issues/1769)
* **core:** fix text alignment in site footer ([ddfbfcc](https://github.com/acdh-oeaw/apis-core-rdf/commit/ddfbfccc2a119c3fc6544684c0060d10c48e32b4)), closes [#1856](https://github.com/acdh-oeaw/apis-core-rdf/issues/1856)
* **generic:** make endpoint enumeration exclude more generic ([cce8851](https://github.com/acdh-oeaw/apis-core-rdf/commit/cce88512f1827158de7106b65f90a2f6ac9ff532))
* **generic:** only run `.mro()` if model is an actual object ([e71177a](https://github.com/acdh-oeaw/apis-core-rdf/commit/e71177a08a1c7c976218a2692e037b0b4c3e62b7))
* **history:** move css class from li element to a element ([3f31b5c](https://github.com/acdh-oeaw/apis-core-rdf/commit/3f31b5c146d980ccb7834e1b93c08928f163e9b9)), closes [#1812](https://github.com/acdh-oeaw/apis-core-rdf/issues/1812)
* **relations:** only check for subj & obj in concrete subclasses ([7fc7495](https://github.com/acdh-oeaw/apis-core-rdf/commit/7fc74952fce1b490c614eb9e4291bd8fedb38c58)), closes [#1837](https://github.com/acdh-oeaw/apis-core-rdf/issues/1837)
* **sample_project:** add migration for history tag removal ([96c508a](https://github.com/acdh-oeaw/apis-core-rdf/commit/96c508a28be6794ac24a6df21aaf9ab7855f44ee))

## [0.45.1](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.45.0...v0.45.1) (2025-04-30)


### Bug Fixes

* **generic:** only use `.split` on strings ([def4348](https://github.com/acdh-oeaw/apis-core-rdf/commit/def434808cb05f07fb69ba74f1c3a76534608e46)), closes [#1840](https://github.com/acdh-oeaw/apis-core-rdf/issues/1840)

## [0.45.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.44.1...v0.45.0) (2025-04-28)


### Features

* **generic:** add a `get_namespace_uri` method to GenericModel ([7af8b83](https://github.com/acdh-oeaw/apis-core-rdf/commit/7af8b8341998cc33d48c6d87b1824f8af4bb82e8))


### Bug Fixes

* **apis_entities:** add margin to bottom of the pills in the lod block ([2b01f34](https://github.com/acdh-oeaw/apis-core-rdf/commit/2b01f34fa44e8bf0dba22521a0713bac4906ff26)), closes [#1773](https://github.com/acdh-oeaw/apis-core-rdf/issues/1773)
* **apis_entities:** fix misspelled verbose_name ([c9e17aa](https://github.com/acdh-oeaw/apis-core-rdf/commit/c9e17aaeb1ad40f412fcb0ac1b2106d596dad4d9)), closes [#1817](https://github.com/acdh-oeaw/apis-core-rdf/issues/1817)
* **generic:** use `.model` instead of `.name.lower()` for prefix ([084528c](https://github.com/acdh-oeaw/apis-core-rdf/commit/084528cc103eafb245e92e0ff8e73b501c70ea0f))
* **relations:** add {suffix}RelationsTable before RelationsTable ([7a4c348](https://github.com/acdh-oeaw/apis-core-rdf/commit/7a4c348d346d048ff68fd36c4e319abaa69a8877)), closes [#1830](https://github.com/acdh-oeaw/apis-core-rdf/issues/1830)
* **relations:** make RelationMultiWidget not use a fieldset ([d9bd5a4](https://github.com/acdh-oeaw/apis-core-rdf/commit/d9bd5a4aeeb05b3d98278ceae874df5c7a3a0373)), closes [#1814](https://github.com/acdh-oeaw/apis-core-rdf/issues/1814)
* **sample_project:** add migration for verbose name update ([8e1b22b](https://github.com/acdh-oeaw/apis-core-rdf/commit/8e1b22bce94e6c35e3236edbaed034ebe24f496c))


### Documentation

* **apis_core:** add basic docstring to urls module ([28aa6ce](https://github.com/acdh-oeaw/apis-core-rdf/commit/28aa6ceb3d91e4b04966f09c40896c9b50115066))
* **apis_metainfo:** add docstring to Uri model ([2b290c1](https://github.com/acdh-oeaw/apis-core-rdf/commit/2b290c10e7c329650dde8dea4d9c9cbe33986dfe))
* **customization:** replace Triple with Relation in model listing ([ccbff74](https://github.com/acdh-oeaw/apis-core-rdf/commit/ccbff74f15161b9f6e042eab03ddc26fe146fdd9))
* **features:** remove documentation of dropped collections features ([87b1501](https://github.com/acdh-oeaw/apis-core-rdf/commit/87b150129342e658501c0eea7e054907a724e1fe))
* **generic:** update importers docstrings, comments ([886f3bf](https://github.com/acdh-oeaw/apis-core-rdf/commit/886f3bf57558e79482b1db480712b0e19208da15))
* **ontology:** drop reference to legacy triples ([f8630aa](https://github.com/acdh-oeaw/apis-core-rdf/commit/f8630aadf7bdf3bf0ce4f2d073896c17557c1365))
* **readme:** drop reference to git logo file ([824df23](https://github.com/acdh-oeaw/apis-core-rdf/commit/824df23afd916857923c5b7f59117ac1afb24917))

## [0.44.1](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.44.0...v0.44.1) (2025-04-17)


### Bug Fixes

* **core:** load i18n templatetags in template ([36ee1e3](https://github.com/acdh-oeaw/apis-core-rdf/commit/36ee1e38b14c6ed0d5bdaa58ed53c49dc99f3d83))

## [0.44.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.43.1...v0.44.0) (2025-04-17)


### ⚠ BREAKING CHANGES

* **collections:** drop `parent` key from collections

### Features

* **apis_entities:** introduce AbstractEntityModelBase ([108482e](https://github.com/acdh-oeaw/apis-core-rdf/commit/108482e3ed46387f2bff1d9668d60cd4467921e1))
* **collections:** drop `parent` key from collections ([1ccddea](https://github.com/acdh-oeaw/apis-core-rdf/commit/1ccddeaa4fc60fcaa00b088d2a6122146699ff7e)), closes [#1603](https://github.com/acdh-oeaw/apis-core-rdf/issues/1603)
* **core:** add select2-bootstrap-5-theme to default stylesheet ([7e2b670](https://github.com/acdh-oeaw/apis-core-rdf/commit/7e2b6701d83b44580ebe19a7be10705ba7801f61))
* **core:** replace icon for code repository ([1a9e7c5](https://github.com/acdh-oeaw/apis-core-rdf/commit/1a9e7c5333ec17fbf7df8813ccb5332eadb5ce78)), closes [#1331](https://github.com/acdh-oeaw/apis-core-rdf/issues/1331)
* **generic:** move css include into the base template ([0288c6d](https://github.com/acdh-oeaw/apis-core-rdf/commit/0288c6da72c333fe3433af8cc5786b942a233eb6))
* **generic:** use gettext for the form submit buttons ([b36aa52](https://github.com/acdh-oeaw/apis-core-rdf/commit/b36aa52ea74bc606b22e9c122060bdda959e36dd))
* **relations:** add check for Meta.ordering to Relation metaclass ([98ac168](https://github.com/acdh-oeaw/apis-core-rdf/commit/98ac168c6aa25c8f28b1f705fdf9d8ea788ffd9f))


### Bug Fixes

* **core:** drop the `User` string in front of the username ([5e31248](https://github.com/acdh-oeaw/apis-core-rdf/commit/5e312487192293342ce83daba256eb0cee7c7ded))
* **core:** use `end` instead of `right` for aligning dropdown ([211135a](https://github.com/acdh-oeaw/apis-core-rdf/commit/211135a6fcb4be56551722b26340cfb892aa2613))
* **core:** use bootstrap5 theme for Select2 widgets ([c01e01c](https://github.com/acdh-oeaw/apis-core-rdf/commit/c01e01cb542d59f177f528e65c3a456bf0152340)), closes [#1754](https://github.com/acdh-oeaw/apis-core-rdf/issues/1754)


### Documentation

* fix import path of README.md ([d197698](https://github.com/acdh-oeaw/apis-core-rdf/commit/d197698d3cfb63524e7085d0f5b915f4c838838e)), closes [#1808](https://github.com/acdh-oeaw/apis-core-rdf/issues/1808)
* **readme:** remove references to poetry from readme ([7a3572d](https://github.com/acdh-oeaw/apis-core-rdf/commit/7a3572d116679b5116cea253d332b9b0c0a38bf5))

## [0.43.1](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.43.0...v0.43.1) (2025-04-15)


### Bug Fixes

* **generic:** make the object-action css classes important ([fadebe9](https://github.com/acdh-oeaw/apis-core-rdf/commit/fadebe95f0d6d25995b5eaa14cf8ac82f3316683)), closes [#1795](https://github.com/acdh-oeaw/apis-core-rdf/issues/1795)
* **generic:** templates: show only existing values ([7103231](https://github.com/acdh-oeaw/apis-core-rdf/commit/71032318a9b04501bccb28c2519b0a02f0148b98)), closes [#1797](https://github.com/acdh-oeaw/apis-core-rdf/issues/1797)

## [0.43.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.42.6...v0.43.0) (2025-04-15)


### ⚠ BREAKING CHANGES

* **collections:** drop code that relies on SkosCollection.parent

### Features

* **apis_core:** inner block in entity_base_nav ([4c1abb5](https://github.com/acdh-oeaw/apis-core-rdf/commit/4c1abb5b8407402291b0a4a5543621f1706e9d25))
* **apis_entities:** open URIs in a new window/tab ([9f75920](https://github.com/acdh-oeaw/apis-core-rdf/commit/9f7592040c8c50de91c9a39c7af6d824e9031731))
* **apis_entities:** ship a CIDOC serializers for E21_Person ([bb7bfad](https://github.com/acdh-oeaw/apis-core-rdf/commit/bb7bfad9b403585c2cc3268c6b1ccc045d96ccf8))
* **documentation:** add menu entry for the documentation app ([826a62b](https://github.com/acdh-oeaw/apis-core-rdf/commit/826a62b41c6e38ca97b6d362e4b071b5d2236ce9)), closes [#1637](https://github.com/acdh-oeaw/apis-core-rdf/issues/1637)
* **generic:** add a GenericModelCidocSerializer ([a8cd90c](https://github.com/acdh-oeaw/apis-core-rdf/commit/a8cd90cefd5e255fca9314ba9b5bf64adc7e2a51))
* **generic:** hide filters that are based on auto_created fields ([e9e9d14](https://github.com/acdh-oeaw/apis-core-rdf/commit/e9e9d14966991583746abcb9719bf531b688bc26))
* **utils:** introduce a apis_base_uri settings helper ([b286bc7](https://github.com/acdh-oeaw/apis-core-rdf/commit/b286bc764ac39b1d3d2a1079e60573f2ba601550))
* **utils:** introduce a rdf_namespace_prefix settings helper ([5e7f93b](https://github.com/acdh-oeaw/apis-core-rdf/commit/5e7f93b7b17291d0b22231d3b9559b0fbcf1ebda))
* **utils:** let config lookup return config if no filter is defined ([a2f4fb9](https://github.com/acdh-oeaw/apis-core-rdf/commit/a2f4fb9af62bfd355f089499c8b6a6376a22532f))
* **utils:** make the `rdf.find_matching_config` method more verbose ([af99368](https://github.com/acdh-oeaw/apis-core-rdf/commit/af99368ae24c393966d7ed0f73d37880c6141c2c))


### Bug Fixes

* **apis_entities:** update translations ([1679ddd](https://github.com/acdh-oeaw/apis-core-rdf/commit/1679ddd2c9d882a684c96a6cb5684ba142aabda5))
* **core:** update translations ([982b953](https://github.com/acdh-oeaw/apis-core-rdf/commit/982b953fadfb048960c5095fedc65ce2f7ba5469))
* **relations:** make default relations abstract ([b44396e](https://github.com/acdh-oeaw/apis-core-rdf/commit/b44396e4e096a1d2503ffb2ba3c52ec1b3dfaf1a))


### Documentation

* cleanup some leftover content from the docs ([1a0e7e5](https://github.com/acdh-oeaw/apis-core-rdf/commit/1a0e7e58fc0f5a4922011ea484ac53fef076cde0))
* move from sphinx to mkdocs ([8b7bc04](https://github.com/acdh-oeaw/apis-core-rdf/commit/8b7bc04802a8bf0220fec33f31bb380b3a0ac7f5))
* spell and style check using vale ([ee8d490](https://github.com/acdh-oeaw/apis-core-rdf/commit/ee8d490eed1073141f2daddb6bf5af750447a37c))


### Code Refactoring

* **collections:** drop code that relies on SkosCollection.parent ([4ac58ad](https://github.com/acdh-oeaw/apis-core-rdf/commit/4ac58ad1fed1a0b2d22206620aa136ebd0ff81f3))

## [0.42.6](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.42.5...v0.42.6) (2025-04-08)


### Bug Fixes

* **generic:** put `extends` at beginning of template ([0ca8402](https://github.com/acdh-oeaw/apis-core-rdf/commit/0ca8402a67fd2ded1f53602a4eeba8ff508b2d0c)), closes [#1761](https://github.com/acdh-oeaw/apis-core-rdf/issues/1761)


### Documentation

* add Sphinx autosectionlabel extension ([777a90a](https://github.com/acdh-oeaw/apis-core-rdf/commit/777a90acc3b1046a1c08896d9c7c8b07feca6473))
* **ontology:** add note regarding history plugin ([48faa9f](https://github.com/acdh-oeaw/apis-core-rdf/commit/48faa9fb2eed5ce8a64895b4174e2d0535aa9fd1)), closes [#1329](https://github.com/acdh-oeaw/apis-core-rdf/issues/1329)

## [0.42.5](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.42.4...v0.42.5) (2025-04-04)


### Bug Fixes

* **collections:** use `.parent_collection` instead of `.parent` ([48372f5](https://github.com/acdh-oeaw/apis-core-rdf/commit/48372f538eac99766cc57fc1125ada4c8e84d17d))

## [0.42.4](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.42.3...v0.42.4) (2025-04-04)


### Bug Fixes

* **apis_entities:** only show map link if there are results ([ca24017](https://github.com/acdh-oeaw/apis-core-rdf/commit/ca2401719253b2dd8e26068c49c7643a73cf4b4d)), closes [#1718](https://github.com/acdh-oeaw/apis-core-rdf/issues/1718)

## [0.42.3](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.42.2...v0.42.3) (2025-04-02)


### Bug Fixes

* **collections:** use blocktranslate with `with` statement ([66eade2](https://github.com/acdh-oeaw/apis-core-rdf/commit/66eade2405fcb452aea035f3f254350fafebec41))
* **generic:** use blocktranslate with with statement ([1400479](https://github.com/acdh-oeaw/apis-core-rdf/commit/1400479ece26422de1bb150d5ca676402e75dc22))
* **templates:** repeat the default settings for htmx.responseHandling ([ac17b83](https://github.com/acdh-oeaw/apis-core-rdf/commit/ac17b836d1b526e44ec6ba6c3d67dd938ee32d70))

## [0.42.2](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.42.1...v0.42.2) (2025-04-02)


### Bug Fixes

* **generic:** load i18n in generic_form template ([48f84f5](https://github.com/acdh-oeaw/apis-core-rdf/commit/48f84f56f326af76ccb2400fb8c93352af68441d))

## [0.42.1](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.42.0...v0.42.1) (2025-04-02)


### Bug Fixes

* **build:** fix project-name that was broken in 0feff6e ([96468e9](https://github.com/acdh-oeaw/apis-core-rdf/commit/96468e91ea56009af877a56a7ec3d15ba27e48ea))

## [0.42.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.41.1...v0.42.0) (2025-04-02)


### Features

* add po files for german translation ([fabcc3b](https://github.com/acdh-oeaw/apis-core-rdf/commit/fabcc3b66201d4c6e70f7cd953039a50dfdb5922))
* **apis_entities:** add metadata & verbose names for abstract models ([e89d5d8](https://github.com/acdh-oeaw/apis-core-rdf/commit/e89d5d80832ea4b514fde1f4f559f4b65f65a586))
* **apis_entities:** use translate blocks for all template stings ([240e1a2](https://github.com/acdh-oeaw/apis-core-rdf/commit/240e1a2b4aa67bda4a80e8e512c02af26c57a692))
* **collections:** use translate blocks for all template stings ([a1e4da0](https://github.com/acdh-oeaw/apis-core-rdf/commit/a1e4da00fdd215992b09d81f3521311ca8fae168))
* **core:** use translate blocks for all template stings ([f03c008](https://github.com/acdh-oeaw/apis-core-rdf/commit/f03c008ed227e7e8c737d31d87cd061554bb922b))
* **documentation:** use translate blocks for all template stings ([45bab12](https://github.com/acdh-oeaw/apis-core-rdf/commit/45bab1223a222bfecb61a6654f30598e859f8537))
* **generic:** print exception message if module not found ([f8b8f85](https://github.com/acdh-oeaw/apis-core-rdf/commit/f8b8f85c2ee06488b603f0a9173832cb8bdd068e))
* **generic:** refactor the generic rdf renderer ([83eb0ab](https://github.com/acdh-oeaw/apis-core-rdf/commit/83eb0abf80eef59b3f3184138cce1bfa6cc1506e))
* **generic:** use translate blocks for all template strings ([d2e4c81](https://github.com/acdh-oeaw/apis-core-rdf/commit/d2e4c818df7652f68cd61189158c79a4cd4a8e22))
* **relations:** use translate blocks for all template stings ([2bfd2a6](https://github.com/acdh-oeaw/apis-core-rdf/commit/2bfd2a6609f0c3f9c4c7631d2dcfb2da572db79f))
* **sample_project:** add migrations based on enhanced entities ([7642671](https://github.com/acdh-oeaw/apis-core-rdf/commit/7642671d0b59e920b3544535eba7fb2015aeb9fa))
* **utils:** allow to pass a language to the rdf importer definition ([23858bb](https://github.com/acdh-oeaw/apis-core-rdf/commit/23858bb93dcb5d4b7bd775cdffbe08c0384aff72))


### Bug Fixes

* tunnel models through importer chain ([dd55edf](https://github.com/acdh-oeaw/apis-core-rdf/commit/dd55edf41101e694cf3b2edce9d3aa0c06a73982)), closes [#1716](https://github.com/acdh-oeaw/apis-core-rdf/issues/1716)


### Documentation

* **readme:** remove deprecated apps from sample config ([2516fc3](https://github.com/acdh-oeaw/apis-core-rdf/commit/2516fc39db46a72378034f51a7ecd06e3c9ab7bc))

## [0.41.1](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.41.0...v0.41.1) (2025-03-27)


### Bug Fixes

* **relations:** work around initial data being empty ([242c6ef](https://github.com/acdh-oeaw/apis-core-rdf/commit/242c6eff4680c6db1768a8c670aea38c0b9a7bca)), closes [#1712](https://github.com/acdh-oeaw/apis-core-rdf/issues/1712)

## [0.41.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.40.1...v0.41.0) (2025-03-26)


### ⚠ BREAKING CHANGES

* **apis_entities:** drop legacy EntityToContenttypeConverter
* **generic:** This change also removes the `id` field from the colums selector, which means it can not be deselected anymore. This is a known issue and we might want to look up a way that *all* the existing table columns (`desc`, `view`, `edit`...) can be deselected.

### Features

* **apis_entities:** adapt place js to also work with lists of points ([71039d5](https://github.com/acdh-oeaw/apis-core-rdf/commit/71039d5f016b24b126873cfc7c2928594c923aba))
* **apis_entities:** add a custom view showing all the places on a map ([623bf50](https://github.com/acdh-oeaw/apis-core-rdf/commit/623bf502bdd828dd3553f7ecf1bca15301494e05)), closes [#1158](https://github.com/acdh-oeaw/apis-core-rdf/issues/1158)
* **apis_entities:** override the list template for e53_place ([1712d68](https://github.com/acdh-oeaw/apis-core-rdf/commit/1712d6863bf82e493abea94081755624b4273c33))
* **apis_entities:** refactor linked_open_data template ([1f22dc0](https://github.com/acdh-oeaw/apis-core-rdf/commit/1f22dc08419246cc7d22592a9e6f572d31dac9f1))
* **apis_entities:** ship SimpleLabelModel ([e64c38f](https://github.com/acdh-oeaw/apis-core-rdf/commit/e64c38ff2f86da182e5a5ac7bb76bc3a65cf6259)), closes [#1686](https://github.com/acdh-oeaw/apis-core-rdf/issues/1686)
* **apis_entities:** use uri shortname in linked_open_data template ([bc39960](https://github.com/acdh-oeaw/apis-core-rdf/commit/bc399607a634c89500a6446fc81ca0e45d923e0e))
* **apis_metainfo:** provide a shortname for Uris ([a73a983](https://github.com/acdh-oeaw/apis-core-rdf/commit/a73a983f74f369ceb71250dce79efa3a494a8ed4))
* **collections:** add CollectionsIncludeExcludeFilter ([26c222d](https://github.com/acdh-oeaw/apis-core-rdf/commit/26c222d027266974f7182447a6047d358672b8dd))
* **generic:** introduce `model_field_template_lookup_list` templatetag ([72d8c93](https://github.com/acdh-oeaw/apis-core-rdf/commit/72d8c93a98af681d1f485c4c30137b1b5f2e814b))
* **generic:** introduce RowColumnMultiValueField + RowColumnMultiWidget ([d7b7d38](https://github.com/acdh-oeaw/apis-core-rdf/commit/d7b7d38c3bd642a2d2c7d7f204df712b5e430a7b))
* **generic:** readd the `get_queryset` method to the List view ([e0465d3](https://github.com/acdh-oeaw/apis-core-rdf/commit/e0465d3d15d8e197fd3eac273dfb0cb57334c00d))
* **generic:** use `model_field_template_lookup_list` for generic table ([2f4b97a](https://github.com/acdh-oeaw/apis-core-rdf/commit/2f4b97a8ea7af729a221caa84e55c17f5e1b20ec))
* **generic:** use CollectionsIncludeExcludeFilter in generic filterset ([d71fd51](https://github.com/acdh-oeaw/apis-core-rdf/commit/d71fd514075d7fc683f5402056ff30e389805b23))
* **relations:** ship some default relations ([b51945c](https://github.com/acdh-oeaw/apis-core-rdf/commit/b51945c8bb4ae749b8416c17c3c60ccb75c6046d)), closes [#1104](https://github.com/acdh-oeaw/apis-core-rdf/issues/1104)


### Bug Fixes

* **apis_entities:** add permission class to GetEntityGeneric view ([d67a782](https://github.com/acdh-oeaw/apis-core-rdf/commit/d67a7826e9d95ec85533de234b4b7b6b5884774b)), closes [#1678](https://github.com/acdh-oeaw/apis-core-rdf/issues/1678)
* **core:** include the main autocomplete_light js in the header ([afa96df](https://github.com/acdh-oeaw/apis-core-rdf/commit/afa96df519a07918e88a1d11dbb3181a7591d541)), closes [#1696](https://github.com/acdh-oeaw/apis-core-rdf/issues/1696)
* **generic:** use different attribute for excluding column choices ([253171a](https://github.com/acdh-oeaw/apis-core-rdf/commit/253171a616ba85e4646728ce818b8e8685c92777))


### Documentation

* **configuration:** correct references to APIS_BASE_URI ([2d13c62](https://github.com/acdh-oeaw/apis-core-rdf/commit/2d13c6274b75bb6d2a8fa4a9aa50a2427e1c3048)), closes [#1680](https://github.com/acdh-oeaw/apis-core-rdf/issues/1680)


### Code Refactoring

* **apis_entities:** drop legacy EntityToContenttypeConverter ([214e634](https://github.com/acdh-oeaw/apis-core-rdf/commit/214e63480c931c268b67457b19dde4a63c16cdc8))

## [0.40.1](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.40.0...v0.40.1) (2025-03-19)


### Bug Fixes

* **generic:** don't coerce values to string in modeldict ([cfbbb92](https://github.com/acdh-oeaw/apis-core-rdf/commit/cfbbb923f61f054a56a925255b2e308b8330bca0))
* **relations:** repair the relation target autocomplete ([5f22e67](https://github.com/acdh-oeaw/apis-core-rdf/commit/5f22e6746e55393f7e64a9160224074b322e0e34)), closes [#1676](https://github.com/acdh-oeaw/apis-core-rdf/issues/1676)
* **utils:** allow to pass an URI string to rdf config filter ([ac6a68f](https://github.com/acdh-oeaw/apis-core-rdf/commit/ac6a68f090b63c8846fe6080dde555bb8545f65c)), closes [#1668](https://github.com/acdh-oeaw/apis-core-rdf/issues/1668)

## [0.40.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.39.0...v0.40.0) (2025-03-11)


### ⚠ BREAKING CHANGES

* **relations:** The refactoring of the relations template tags leads to a slightly different behaviour in the lookup of the relations tables; please have a look at the lookup debug statements if your relations tables are not found anymore.
* **utils:** drop the DateParser and the corresponding tests
* **core:** drop LegacyDateMixin

### Features

* **apis_metainfo:** adapt Uri model for new type rdf import ([4184584](https://github.com/acdh-oeaw/apis-core-rdf/commit/41845848193c103c408b06c561d3dd6e28a4800e))
* **generic:** adapt importer for new type rdf import methods ([db6f4bf](https://github.com/acdh-oeaw/apis-core-rdf/commit/db6f4bff2591228f0e97d055d14a4a412cf3dbe5))
* **generic:** introduce new templatetags ([37f8f11](https://github.com/acdh-oeaw/apis-core-rdf/commit/37f8f11d92a0d405c05d79f43837b56900b28bb4))
* **generic:** introduce small helper functions ([2b6bef8](https://github.com/acdh-oeaw/apis-core-rdf/commit/2b6bef83754baf4339cf0698c1e833eb00ba2c88))
* **relations:** implement a relation filter ([5f56b45](https://github.com/acdh-oeaw/apis-core-rdf/commit/5f56b455825236c32998d08cf367f78a79e6993f))
* **relations:** major rewrite of the relations list ([29d39da](https://github.com/acdh-oeaw/apis-core-rdf/commit/29d39dab2644980f51c7d09a6a24695e4b8cdde5))
* **sample_project:** update sample project for new relation templates ([c1f293c](https://github.com/acdh-oeaw/apis-core-rdf/commit/c1f293cecaa8e6c5a97a8d1e5236517b85fd5c14))
* **utils:** drop old rdf import methods ([0852822](https://github.com/acdh-oeaw/apis-core-rdf/commit/0852822075eadbd705ee635dd925baee6a4340a3))
* **utils:** implement new type rdf importer ([73e738e](https://github.com/acdh-oeaw/apis-core-rdf/commit/73e738e118462db605b88dacf5dd58327232d680))


### Bug Fixes

* **apis_entities:** fix entities autocomplete ([dcc479b](https://github.com/acdh-oeaw/apis-core-rdf/commit/dcc479be754737b515d951245de4dad602a36243))
* **apis_entities:** reorder entity menu items ([cb242cf](https://github.com/acdh-oeaw/apis-core-rdf/commit/cb242cf6e8e9e5299ece510f73b86d09d9bdb52c)), closes [#1657](https://github.com/acdh-oeaw/apis-core-rdf/issues/1657)
* **apis_metainfo:** drop references to `apis_metainfo.collection` ([2a7500e](https://github.com/acdh-oeaw/apis-core-rdf/commit/2a7500e55b69b9c686a15d2f7cd647f1111fc5bb)), closes [#1377](https://github.com/acdh-oeaw/apis-core-rdf/issues/1377)
* **collections:** repair the new collection toggle templatetags ([c3f4f6b](https://github.com/acdh-oeaw/apis-core-rdf/commit/c3f4f6be26cf22d6a2110382db07ea6f842e2deb))
* **generic:** show form errors of generic filter form ([d8e81c8](https://github.com/acdh-oeaw/apis-core-rdf/commit/d8e81c8bcac484bb06f7f51e6faec28bd6dbdaaa)), closes [#1604](https://github.com/acdh-oeaw/apis-core-rdf/issues/1604)


### Documentation

* **customization:** add documentation about new rdf parser ([c51ada4](https://github.com/acdh-oeaw/apis-core-rdf/commit/c51ada4503247374557d99b47688646e3e3413a5))


### Code Refactoring

* **core:** drop LegacyDateMixin ([7a1d940](https://github.com/acdh-oeaw/apis-core-rdf/commit/7a1d9401eafec33869f8818e79a80d7b5da94b35))
* **utils:** drop the DateParser and the corresponding tests ([5325d46](https://github.com/acdh-oeaw/apis-core-rdf/commit/5325d46a1f08cb530d9c72a4df2223a9caeeb353))

## [0.39.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.38.0...v0.39.0) (2025-02-28)


### ⚠ BREAKING CHANGES

* **apis_metainfo:** The `self_contenttype` field is removed from the RootObject. This means that all models inheriting from RootObject (i.e. all models inheriting from AbstractEntity) loose this field. For the models using the VersionMixin, this leads to a migration removing the `self_contenttype` field from the historic version of that model.

### Features

* **apis_entities:** add a feature code field to E53_Place ([f8867db](https://github.com/acdh-oeaw/apis-core-rdf/commit/f8867dbbdac452bf11c0a033e4d49986cb0ff482))
* **apis_entities:** replace entity list templatetag with generic one ([0d1abd6](https://github.com/acdh-oeaw/apis-core-rdf/commit/0d1abd607edc1348f0efdcc2650f2eaeb74a5ea2)), closes [#1576](https://github.com/acdh-oeaw/apis-core-rdf/issues/1576)
* **apis_metainfo:** drop `self_contenttype` field from RootObject ([cf2ea10](https://github.com/acdh-oeaw/apis-core-rdf/commit/cf2ea10b363152b377543d4e168dda3c715364e4))
* **apis_vocabularies:** drop apis_vocabularies app ([3602f85](https://github.com/acdh-oeaw/apis-core-rdf/commit/3602f85c34f161315c261d9b83e047888813435b))
* **collections:** implement toggling collection without the parent ([1d63c15](https://github.com/acdh-oeaw/apis-core-rdf/commit/1d63c156364913855db8d33560c3624458edc05a))
* **core:** update htmx script inclusion to v2.0.4 ([0e63150](https://github.com/acdh-oeaw/apis-core-rdf/commit/0e631503c01b6f5393682ad1adec1a01dbb34758)), closes [#1606](https://github.com/acdh-oeaw/apis-core-rdf/issues/1606)
* **generic:** allow to inject additional modules into lookup path ([fa9ede2](https://github.com/acdh-oeaw/apis-core-rdf/commit/fa9ede2b8b06a637162cb5679e857bd945b0e94a))
* **generic:** fallback to custom create method if value is not an URI ([15831c1](https://github.com/acdh-oeaw/apis-core-rdf/commit/15831c1251c197e1b6609f043071b36840e94035))
* **generic:** introduce a `content_type` property on GenericModel ([c103b90](https://github.com/acdh-oeaw/apis-core-rdf/commit/c103b90703352a546e75a873dfefed1e4d790c7f))
* **relations:** remove relation_ptr from columns selector ([a697a78](https://github.com/acdh-oeaw/apis-core-rdf/commit/a697a78fc39764b46bf39c43774b4cc0b8d03a5d)), closes [#1612](https://github.com/acdh-oeaw/apis-core-rdf/issues/1612)
* **relations:** replace `self_contenttype` with `content_type` property ([31c7191](https://github.com/acdh-oeaw/apis-core-rdf/commit/31c7191405a6d37259dbb090c6422997101bb28e))
* **relations:** replace relation list template tag with generic one ([79d8691](https://github.com/acdh-oeaw/apis-core-rdf/commit/79d8691bf099c43b1a61e112a900bd1f295b6477)), closes [#1577](https://github.com/acdh-oeaw/apis-core-rdf/issues/1577)
* **sample_project:** add migration introducing E53_Place.feature_code ([3458a7f](https://github.com/acdh-oeaw/apis-core-rdf/commit/3458a7fa01a30a69d7adcab9b852fe8eed98c3be))
* **sample_project:** add migration that drops `self_contenttype` ([ed02d02](https://github.com/acdh-oeaw/apis-core-rdf/commit/ed02d02eabd32886dae3bc61c23a7d90f62288e8))
* **sample_project:** move generic app up in INSTALLED_APPS list ([321a061](https://github.com/acdh-oeaw/apis-core-rdf/commit/321a06119f80be762fe94b2822ca9019ceca0fd3))


### Bug Fixes

* **generic:** don't show subclasses in columns selector ([37e9170](https://github.com/acdh-oeaw/apis-core-rdf/commit/37e9170705ceb7e5d7ed20060859108f50c440d2)), closes [#1297](https://github.com/acdh-oeaw/apis-core-rdf/issues/1297)
* **generic:** remove many2many relation tables from columns ([82235c7](https://github.com/acdh-oeaw/apis-core-rdf/commit/82235c76f0e125b8fade3bdf159c7af0e568d70e)), closes [#1500](https://github.com/acdh-oeaw/apis-core-rdf/issues/1500)
* **generic:** use verbose_name_plural for generic menu items ([d3f4c8c](https://github.com/acdh-oeaw/apis-core-rdf/commit/d3f4c8c9f53b3d1b87ea9e0861fb939997aad7f9)), closes [#1624](https://github.com/acdh-oeaw/apis-core-rdf/issues/1624)
* **sample_project:** drop self_contenttype from fixtures ([e77665a](https://github.com/acdh-oeaw/apis-core-rdf/commit/e77665ad5d2d6712681659ea44d0b7075ce1e3d4)), closes [#1633](https://github.com/acdh-oeaw/apis-core-rdf/issues/1633)

## [0.38.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.37.2...v0.38.0) (2025-02-18)


### Features

* **apis_relations:** drop `apis_relations` app ([31a37b6](https://github.com/acdh-oeaw/apis-core-rdf/commit/31a37b6ecc670be8d00f48340c88f2a65c0f6359)), closes [#1528](https://github.com/acdh-oeaw/apis-core-rdf/issues/1528)
* **core:** introduce a custom select2 function ([0468c3f](https://github.com/acdh-oeaw/apis-core-rdf/commit/0468c3f809c4aa2a48e69b466f573d1e0920cd63))
* **generic:** add `get_view_permission` to GenericModel ([a3fb75d](https://github.com/acdh-oeaw/apis-core-rdf/commit/a3fb75da37d52b34bee1aa9cf9b652e40626aa64))
* **generic:** introduce `pure_genericmodel_content_types` templatetag ([eaf7d5a](https://github.com/acdh-oeaw/apis-core-rdf/commit/eaf7d5a8c2a4d5591e7a03d85760fbce72261fe5))
* **generic:** introduce any_view_permission templatetag ([4c35738](https://github.com/acdh-oeaw/apis-core-rdf/commit/4c357384ed7807f0b3084fedff5cd9a8557d4814))
* **generic:** override base.html to inject menu entry ([54a5b37](https://github.com/acdh-oeaw/apis-core-rdf/commit/54a5b378f00844972d1c7d768b1118b139253637))
* **generic:** use custom autocomplete widgets instead of upstreams ([bd9e49a](https://github.com/acdh-oeaw/apis-core-rdf/commit/bd9e49a81fe317b6dc9df94d4b4eaf7e964c824c))
* **relations:** replace custom select2 call ([7377e38](https://github.com/acdh-oeaw/apis-core-rdf/commit/7377e388a5a58ff1972a1a75ab8f9cbb93214637))
* **relations:** use custom autocomplete widgets instead of upstreams ([ae7dfba](https://github.com/acdh-oeaw/apis-core-rdf/commit/ae7dfba2d4e04a2b583c0927975287283352f23f))


### Bug Fixes

* **apis_entities:** drop `apis_relation` related code parts ([4962949](https://github.com/acdh-oeaw/apis-core-rdf/commit/49629494c1e5111e96a70a7c1e72cba3b6fd923a))
* **documentation:** drop `apis_relation` related code parts ([3f06425](https://github.com/acdh-oeaw/apis-core-rdf/commit/3f064250db0248bd231f19f17a589bcf4d5a6785))
* **generic:** set unknown_field_behavior to WARN in GenericFilterSet ([291cb14](https://github.com/acdh-oeaw/apis-core-rdf/commit/291cb1494b0140fc492e6bd9980c8382d43c3945)), closes [#1583](https://github.com/acdh-oeaw/apis-core-rdf/issues/1583)
* **history:** drop `apis_relation` related code parts ([e588c70](https://github.com/acdh-oeaw/apis-core-rdf/commit/e588c7079a5c49f658c7e1ca553d14b6fa9f7d4a)), closes [#1536](https://github.com/acdh-oeaw/apis-core-rdf/issues/1536)
* **urls:** drop `apis_relations` entry from urllist ([09b7fea](https://github.com/acdh-oeaw/apis-core-rdf/commit/09b7fea9d43dd1860d6c1e652e24de78e7415f33))


### Documentation

* **features:** fix typo ([0381d59](https://github.com/acdh-oeaw/apis-core-rdf/commit/0381d598960e9e1bdd27acc79099568c69619618)), closes [#1589](https://github.com/acdh-oeaw/apis-core-rdf/issues/1589)

## [0.37.2](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.37.1...v0.37.2) (2025-02-05)


### Bug Fixes

* **generic:** move split up again and put it inside try/except ([543d6ae](https://github.com/acdh-oeaw/apis-core-rdf/commit/543d6ae79776dbeaab0bd3c279b684ae59ab67fb))

## [0.37.1](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.37.0...v0.37.1) (2025-02-05)


### Bug Fixes

* **generic:** only split value if it actually exists ([997975c](https://github.com/acdh-oeaw/apis-core-rdf/commit/997975c64387fe825e8893f6b22ecc7d9c869239))

## [0.37.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.36.1...v0.37.0) (2025-02-05)


### Features

* **apis_entities:** move entities menu to apis_entities app ([cf73280](https://github.com/acdh-oeaw/apis-core-rdf/commit/cf732801edd19918ac3fd5acf9595fa51a99e927))
* **collections:** add `Collections` entry to main menu ([954e49d](https://github.com/acdh-oeaw/apis-core-rdf/commit/954e49def98b6e2a6f20f5847db74341302abbb6)), closes [#1565](https://github.com/acdh-oeaw/apis-core-rdf/issues/1565)
* **core:** enclose user-menu items in a block ([4ef987c](https://github.com/acdh-oeaw/apis-core-rdf/commit/4ef987cad7d10d50a9ca63297288f91729343459))
* **core:** include bootstrap 5.3.3 instead of bootstrap 4.6.2 ([5dc28e9](https://github.com/acdh-oeaw/apis-core-rdf/commit/5dc28e9a69607f97b890598dc471e402a97aa039)), closes [#1529](https://github.com/acdh-oeaw/apis-core-rdf/issues/1529)
* **generic:** add a collections filter ([501ab78](https://github.com/acdh-oeaw/apis-core-rdf/commit/501ab780fbc3766f747a58825c47c4af5faf401a)), closes [#1557](https://github.com/acdh-oeaw/apis-core-rdf/issues/1557)
* **generic:** add export support to list views ([c8c7670](https://github.com/acdh-oeaw/apis-core-rdf/commit/c8c76708bc42dfc9503c9dbf9e95da01f4a08425))
* **relations:** move relations menu to relations app ([b04b8f9](https://github.com/acdh-oeaw/apis-core-rdf/commit/b04b8f91cecde554a8f1ce62dcd3e6e48b737671))
* **sample_project:** configure sample project to use bootstrap 5 ([aca77f6](https://github.com/acdh-oeaw/apis-core-rdf/commit/aca77f6e94807e46f5f097b00efde4045d0123aa))


### Bug Fixes

* adapt templates for bootstrap version 5 ([6e771bf](https://github.com/acdh-oeaw/apis-core-rdf/commit/6e771bf48bc4577bc42a261cd8beafe4788ee736))
* **core:** adapt multiselect settings for bootstrap 5 ([6bc99fe](https://github.com/acdh-oeaw/apis-core-rdf/commit/6bc99fe2f091c76f257a544faead5d169755e9e5))
* **relations:** hide empty relations tables ([8f13605](https://github.com/acdh-oeaw/apis-core-rdf/commit/8f13605ad3405c59039c1c3746763f1d6e353520)), closes [#1543](https://github.com/acdh-oeaw/apis-core-rdf/issues/1543)

## [0.36.1](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.36.0...v0.36.1) (2025-01-27)


### Bug Fixes

* **generic:** only add collections if app is installed ([a709d33](https://github.com/acdh-oeaw/apis-core-rdf/commit/a709d337dc4e7f41912f8ac6525168819c56a635)), closes [#1554](https://github.com/acdh-oeaw/apis-core-rdf/issues/1554)

## [0.36.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.35.1...v0.36.0) (2025-01-23)


### ⚠ BREAKING CHANGES

* **utils:** let the rdf parser return lists instead of strings
* **utils:** drop unused module `apis_core.utils.normalize`

### Features

* **collections:** add some helper methods to SkosCollection + Manager ([372a5ae](https://github.com/acdh-oeaw/apis-core-rdf/commit/372a5ae9a3b68216e3171cb2bcd1116e22aa47f7))
* **generic:** adapt importer to rdf parser list style return values ([2a2cdfd](https://github.com/acdh-oeaw/apis-core-rdf/commit/2a2cdfdb31473c04d4e84afa57852dcd1b2d103c))
* **generic:** add a form field for managing collections for an instance ([e0f7961](https://github.com/acdh-oeaw/apis-core-rdf/commit/e0f7961cbd52449bcd64c9a56fe00f9a18373405)), closes [#1532](https://github.com/acdh-oeaw/apis-core-rdf/issues/1532)
* switch from custom uri normalization to acdh-arche-assets ([83c0737](https://github.com/acdh-oeaw/apis-core-rdf/commit/83c07374df44f61aa048e46d8c55d36108c6dc7d)), closes [#1531](https://github.com/acdh-oeaw/apis-core-rdf/issues/1531)
* **utils:** let the rdf parser return lists instead of strings ([aa1b6ed](https://github.com/acdh-oeaw/apis-core-rdf/commit/aa1b6ed254d80cbe882267ae59316eebeedfb5f9))


### Bug Fixes

* **relations:** refactor js and add it to forms Media class ([5e4a9c0](https://github.com/acdh-oeaw/apis-core-rdf/commit/5e4a9c04b3bd882a8afd84729b48bcc7f7e9924b)), closes [#1544](https://github.com/acdh-oeaw/apis-core-rdf/issues/1544)


### Miscellaneous Chores

* **utils:** drop unused module `apis_core.utils.normalize` ([ad54c56](https://github.com/acdh-oeaw/apis-core-rdf/commit/ad54c5609b43120b578dd311183195a87cff701c))

## [0.35.1](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.35.0...v0.35.1) (2025-01-10)


### Bug Fixes

* **apis_metainfo:** check for numeric id before iterating related Uris ([a909428](https://github.com/acdh-oeaw/apis-core-rdf/commit/a90942853bedcbe5cd4ee801c9ac86c7b732df34))

## [0.35.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.34.1...v0.35.0) (2025-01-08)


### ⚠ BREAKING CHANGES

* **generic:** APIS_LIST_VIEWS_ALLOWED and APIS_DETAIL_VIEWS_ALLOWED are replaced with a single setting APIS_ANON_VIEWS_ALLOWED When APIS_ANON_VIEWS_ALLOWED is set to True List views and Detail views will be open to anyone, without having to login. APIS_LIST_VIEW_OBJECT_FILTER and APIS_VIEW_PASSES_TEST are no longer supported. Custom managers should be used instead.
* **generic,apis_metainfo:** move duplicate signals to generic app

### Features

* **apis_entities:** update `create_default_uri` to use generic uri ([2050de3](https://github.com/acdh-oeaw/apis-core-rdf/commit/2050de3acb5fd83ab29769f72246ad5d601403a4))
* **apis_metainfo:** add a signal to remove unused Uris ([e64182c](https://github.com/acdh-oeaw/apis-core-rdf/commit/e64182c630086432764719517969b4db7061f430))
* **apis_metainfo:** replace Uri.root_object with GenericForeignKey ([43aec8b](https://github.com/acdh-oeaw/apis-core-rdf/commit/43aec8b3c0572774601a886d21c10c83ad56a59c))
* **apis_relations:** update GenericTripleForm to work with generic uri ([e4e5616](https://github.com/acdh-oeaw/apis-core-rdf/commit/e4e5616fa02b4e5dba7653d28a306daa49b3136c))
* **core:** introduce a MaintenanceMiddleware ([dc0cda0](https://github.com/acdh-oeaw/apis-core-rdf/commit/dc0cda03c59c9fff24224543f5c2a4bc6bb5426f)), closes [#1296](https://github.com/acdh-oeaw/apis-core-rdf/issues/1296)
* **generic:** add `uri_set` method to GenericModel ([a95c076](https://github.com/acdh-oeaw/apis-core-rdf/commit/a95c0767b19602b6bbb3b935797335df69e6c2f1))
* **generic:** add a `get_openapi_tags` class method ([512f769](https://github.com/acdh-oeaw/apis-core-rdf/commit/512f7692698b898356324ebd9495fcb43052ce15))
* **generic:** APIS_ANON_VIEWS_ALLOWED setting ([f2e0b2f](https://github.com/acdh-oeaw/apis-core-rdf/commit/f2e0b2f9ac5f43154049284529e9ec9e1af393c7)), closes [#1400](https://github.com/acdh-oeaw/apis-core-rdf/issues/1400)
* **generic:** introduce custom AutoSchema for schema customization ([7b4646d](https://github.com/acdh-oeaw/apis-core-rdf/commit/7b4646df5f4d9756a6be74cb900e63f9176369dd))
* **generic:** update Enrichview & GenericModel to work with generic uri ([c5dbc80](https://github.com/acdh-oeaw/apis-core-rdf/commit/c5dbc80f16a5a3e8d1cb39f5a8e9e7380df1c0f5))
* **generic:** use GenericAutoSchema in ModelViewSet ([454de2f](https://github.com/acdh-oeaw/apis-core-rdf/commit/454de2fa0281e2f0b3df6b1260884c34962420a5))
* **utils:** update create_object_from_uri to work with generic uri ([1ccfffe](https://github.com/acdh-oeaw/apis-core-rdf/commit/1ccfffe8525b0397349a4e022c32e26cabe9acba))


### Bug Fixes

* **generic:** remove .html from template_name_suffix ([9944661](https://github.com/acdh-oeaw/apis-core-rdf/commit/994466155def462374a95d96aad2b65cd6837ef7))


### Documentation

* add documentation regarding MaintenanceMiddleware ([516b07c](https://github.com/acdh-oeaw/apis-core-rdf/commit/516b07c9f16a0cb5075947346fa69b4e6dc89a8d))
* **configuration:** add APIS_FORMER_BASE_URIS setting ([46223a9](https://github.com/acdh-oeaw/apis-core-rdf/commit/46223a908eea25c5cfefa040ac62bbd168e0e4eb))
* **configuration:** update configs for anonymous views ([6f28df6](https://github.com/acdh-oeaw/apis-core-rdf/commit/6f28df6a83ce3f2a2059f52c01b2de7b9f0d35c2))


### Code Refactoring

* **generic,apis_metainfo:** move duplicate signals to generic app ([3e20f06](https://github.com/acdh-oeaw/apis-core-rdf/commit/3e20f067e7ff412547ef0d2534e4eadb585789fc))

## [0.34.1](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.34.0...v0.34.1) (2024-12-11)


### Bug Fixes

* **relations:** only filter queryset if there is actually a value ([7cd93e7](https://github.com/acdh-oeaw/apis-core-rdf/commit/7cd93e70f27ba97cfc7cb95bd324ee2ebd0bac15))
* **relations:** only serialize if there is an object ([163f3f8](https://github.com/acdh-oeaw/apis-core-rdf/commit/163f3f85472841de3e553c2042fb89a2da863976))


### Documentation

* **history:** add documentation on some management commands ([320e73f](https://github.com/acdh-oeaw/apis-core-rdf/commit/320e73f8a83df38103fa64694b4548382b4852e2)), closes [#873](https://github.com/acdh-oeaw/apis-core-rdf/issues/873)
* **history:** add section on middleware for user tracking ([4694885](https://github.com/acdh-oeaw/apis-core-rdf/commit/4694885f6278d76e2a54a7daf248678dd7ee779d))

## [0.34.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.33.0...v0.34.0) (2024-12-09)


### Features

* **apis_entities:** replace apis_entities merge route ([40e4618](https://github.com/acdh-oeaw/apis-core-rdf/commit/40e461826911059c85742b5cb66a76c37fdda373))
* **apis_entities:** reuse legacy _merge template ([10c524e](https://github.com/acdh-oeaw/apis-core-rdf/commit/10c524ef36da57924b738cc92cc230cf5a28a3ec))
* **apis_metainfo:** add a `internal` method to the Uri ([a65617e](https://github.com/acdh-oeaw/apis-core-rdf/commit/a65617eecdcd974474b3936abd4062b9dedbc82b))
* **core:** add additional settings of bootstrap-multiselect ([012e1d1](https://github.com/acdh-oeaw/apis-core-rdf/commit/012e1d18ed04c6844a6528ab3aed7f0ce646dd3c))
* **core:** drop inclusion of select2 javascript and css ([3d53102](https://github.com/acdh-oeaw/apis-core-rdf/commit/3d5310202ab3e6e3c9624d436ae99053459e4f54)), closes [#1481](https://github.com/acdh-oeaw/apis-core-rdf/issues/1481)
* **core:** update bootstrap-multiselect dependency ([4fdd848](https://github.com/acdh-oeaw/apis-core-rdf/commit/4fdd848f626475f328f0cb7fee28316475fe915b))
* **generic:** Introduce SelectMergeOrEnrich view and route ([fb07e49](https://github.com/acdh-oeaw/apis-core-rdf/commit/fb07e49ee0753924bac25953a06754ff24b96ccf))
* **utils:** introduce an `internal_uris` settings helper ([bb1e7a3](https://github.com/acdh-oeaw/apis-core-rdf/commit/bb1e7a3af2691223243da78e9560ffb9dab47d13))


### Bug Fixes

* **apis_entities:** disable create_default_uri during fixture loading ([f604816](https://github.com/acdh-oeaw/apis-core-rdf/commit/f6048161bb87d00b0e617a16de1e01a5b4a99590)), closes [#1473](https://github.com/acdh-oeaw/apis-core-rdf/issues/1473)
* **apis_entities:** show enrich link only for external URIs ([8aea255](https://github.com/acdh-oeaw/apis-core-rdf/commit/8aea2556c89febea11eaf5a7e0c27d72d012502e))
* **generic,apis_entities:** move action classes to generic app ([ff58a98](https://github.com/acdh-oeaw/apis-core-rdf/commit/ff58a987a3fb78026ac3b5b4c51b8918ea04b3c5)), closes [#1469](https://github.com/acdh-oeaw/apis-core-rdf/issues/1469)
* **generic:** catch exception if .template_name is not set ([91f7c77](https://github.com/acdh-oeaw/apis-core-rdf/commit/91f7c7768a3f410c9ab4841a8b509e74942dd382))
* **generic:** exclude subclasses from columns selector ([14dcb6f](https://github.com/acdh-oeaw/apis-core-rdf/commit/14dcb6f674b319df89d4976c0aed0df9fd754bf3)), closes [#1297](https://github.com/acdh-oeaw/apis-core-rdf/issues/1297)

## [0.33.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.32.0...v0.33.0) (2024-11-27)


### ⚠ BREAKING CHANGES

* **generic:** replace `object_table.html` by template_list lookup

### Features

* **generic:** add a templatetag wrapper for template_names_via_mro ([9605817](https://github.com/acdh-oeaw/apis-core-rdf/commit/9605817e04674e1c91338acec515dbd7234d93ae))
* **generic:** allow to disable pagination in table class ([e275e59](https://github.com/acdh-oeaw/apis-core-rdf/commit/e275e59be75e25fe92c1b8e4127f6667e6861e29)), closes [#1444](https://github.com/acdh-oeaw/apis-core-rdf/issues/1444)
* **relations:** limit the number of subj/obj models in filter ([6e6d026](https://github.com/acdh-oeaw/apis-core-rdf/commit/6e6d026a1df0d4f682a43d9abdff61a9810b2a73)), closes [#1390](https://github.com/acdh-oeaw/apis-core-rdf/issues/1390)


### Bug Fixes

* **apis_entities:** change icon for enrich functionality ([2b44bce](https://github.com/acdh-oeaw/apis-core-rdf/commit/2b44bce4f36db165767bb9a4a74e467377512c69)), closes [#1439](https://github.com/acdh-oeaw/apis-core-rdf/issues/1439)
* **apis_entities:** replace the update link icon with text ([c30eded](https://github.com/acdh-oeaw/apis-core-rdf/commit/c30eded4b469e7b4060434f790d7cc76c862fd5b))
* **core:** harmonize footer icon dimension specification ([624d74a](https://github.com/acdh-oeaw/apis-core-rdf/commit/624d74a1d300973876cc5012e7b7dc0c3dff7115)), closes [#1340](https://github.com/acdh-oeaw/apis-core-rdf/issues/1340)
* **generic:** check for attribute `id` before using it ([076e9f3](https://github.com/acdh-oeaw/apis-core-rdf/commit/076e9f361e4c98e74afe264924086bb75b9cea8e)), closes [#1450](https://github.com/acdh-oeaw/apis-core-rdf/issues/1450)
* **generic:** replace `object_table.html` by template_list lookup ([055ec94](https://github.com/acdh-oeaw/apis-core-rdf/commit/055ec94af98234b48153a83752869270e1a6a453)), closes [#1446](https://github.com/acdh-oeaw/apis-core-rdf/issues/1446)


### Documentation

* **changelog:** replace wrong bug number with correct one ([36c97b1](https://github.com/acdh-oeaw/apis-core-rdf/commit/36c97b1a7574f18b258ad4bc158c86d7eecf2328)), closes [#1376](https://github.com/acdh-oeaw/apis-core-rdf/issues/1376)
* **customization:** document the `table_pagination` setting ([9e35eb7](https://github.com/acdh-oeaw/apis-core-rdf/commit/9e35eb7f4a09fd4a74ef58ccf208b6f5ed0d92a4))
* **customization:** fix typos `you_app` -&gt; `your_app` ([e3445d9](https://github.com/acdh-oeaw/apis-core-rdf/commit/e3445d9bc87dbb1d7408455835a0d568de4962c2))
* **customization:** replace `apis_ontology` with `your_app` ([06a960e](https://github.com/acdh-oeaw/apis-core-rdf/commit/06a960eb83b2b6bc69315f25928e72cf58a545cd))
* point Django documentation links to stable version ([f87ad58](https://github.com/acdh-oeaw/apis-core-rdf/commit/f87ad58f1e25314d8ab10dffc7b717e59665e38b))
* **README:** point Django documentation links to stable version ([8accb2b](https://github.com/acdh-oeaw/apis-core-rdf/commit/8accb2bb20fcda0b0d42037082b735c9318a5dbd))
* **README:** replace note about models.py with link to the docs ([f8bb514](https://github.com/acdh-oeaw/apis-core-rdf/commit/f8bb51499fe1da61d925a46db5698a09fa3d7ba8))
* remove `django-admin-csvexport` from list of dependencies ([96dd125](https://github.com/acdh-oeaw/apis-core-rdf/commit/96dd125219fc9de999759cd7e11dcd25db7aa42e))

## [0.32.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/apis-core-rdf-v0.31.1...apis-core-rdf-v0.32.0) (2024-11-20)


### ⚠ BREAKING CHANGES

* **utils:** drop unused `utils.utils` module
* **core:** drop unused ViewPassesTestMixin

### Features

* **apis_entities:** allow to paste string in merge form ([6b44299](https://github.com/acdh-oeaw/apis-core-rdf/commit/6b44299dfc253053c565e432cb3271d66a107db6))
* **generic:** allow to paste a string in the import form ([41cb229](https://github.com/acdh-oeaw/apis-core-rdf/commit/41cb229ce49b07e5fba5ea3f3b3834e3242c10aa)), closes [#1223](https://github.com/acdh-oeaw/apis-core-rdf/issues/1223)
* **relations:** put display logic of relations in a block ([0d71f8f](https://github.com/acdh-oeaw/apis-core-rdf/commit/0d71f8fde8c6d95f326b4ab67bd7455788389e6e))


### Bug Fixes

* **apis_entities:** remove merge form from the entities edit view ([2b0dcf1](https://github.com/acdh-oeaw/apis-core-rdf/commit/2b0dcf11792c766e72f7cfb487d65dffd54a289d)), closes [#1285](https://github.com/acdh-oeaw/apis-core-rdf/issues/1285)
* **core:** remove leading slash from static files ([d657a98](https://github.com/acdh-oeaw/apis-core-rdf/commit/d657a9843ccf79f2caf2059654e86af26bbc7f36)), closes [#1339](https://github.com/acdh-oeaw/apis-core-rdf/issues/1339)
* **generic:** run the columns names through `pretty_name` ([07951c4](https://github.com/acdh-oeaw/apis-core-rdf/commit/07951c400757185b948813a2dc56ab725117c3a7)), closes [#1028](https://github.com/acdh-oeaw/apis-core-rdf/issues/1028)
* **generic:** use a URL param to enable autocomplete create function ([6995a73](https://github.com/acdh-oeaw/apis-core-rdf/commit/6995a73d6722f379f0d2cb0f22658fb47901e1b8))
* **history:** drop TempTripleHistoryLogs api view ([b754e68](https://github.com/acdh-oeaw/apis-core-rdf/commit/b754e68f9d1f5d7e134eda7971cdef7910b2b274))
* **relations:** support modelselect2 fields ([b7ba802](https://github.com/acdh-oeaw/apis-core-rdf/commit/b7ba80266b7bebc90ebe3034b5e5f8689833caee))
* **utils:** add a `raise_on_fail` argument to the object create function ([16c2ef7](https://github.com/acdh-oeaw/apis-core-rdf/commit/16c2ef726e888deec5d6f3a0475b92f6392314fc)), closes [#1405](https://github.com/acdh-oeaw/apis-core-rdf/issues/1405)
* **utils:** raise exception on failing creation of object ([d93a17d](https://github.com/acdh-oeaw/apis-core-rdf/commit/d93a17d7782c950968e189554e1b338aa06a7c76))


### Miscellaneous Chores

* **core:** drop unused ViewPassesTestMixin ([ed3dfa0](https://github.com/acdh-oeaw/apis-core-rdf/commit/ed3dfa0dadcbd9a3603bb20bb4c2ea4b34bf18b8))
* **utils:** drop unused `utils.utils` module ([734ec4c](https://github.com/acdh-oeaw/apis-core-rdf/commit/734ec4c8d8343f54655eefbabb789b926d728878))

## [0.31.1](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.31.0...v0.31.1) (2024-11-14)


### Bug Fixes

* **apis_entities:** set target of merge link to correct route ([5b200ed](https://github.com/acdh-oeaw/apis-core-rdf/commit/5b200ed245159780b37b24e61720265c7653ac58)), closes [#1374](https://github.com/acdh-oeaw/apis-core-rdf/issues/1374)

## [0.31.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.30.0...v0.31.0) (2024-11-13)


### Features

* **core:** add alt attributes to footer images ([cfa9006](https://github.com/acdh-oeaw/apis-core-rdf/commit/cfa9006472d59ad8e544173b85cb2bf7d28a2ffa))
* **sample_project:** demo a long relations form ([cb80dd3](https://github.com/acdh-oeaw/apis-core-rdf/commit/cb80dd3ca5199860ecda860782e16d495ed02660))


### Bug Fixes

* **core:** fix dimensions of links in footer ([c2c5594](https://github.com/acdh-oeaw/apis-core-rdf/commit/c2c5594cc73dd61eb5b6a42aa402c2c3d98bec6b))
* **generic:** use copy instead of working with the original field ([1fec441](https://github.com/acdh-oeaw/apis-core-rdf/commit/1fec441289b95b3bdfdc771f44929986fd47ce52)), closes [#1346](https://github.com/acdh-oeaw/apis-core-rdf/issues/1346)
* **relations:** fix modal overflow to access dropdown ([e14c806](https://github.com/acdh-oeaw/apis-core-rdf/commit/e14c8060672744076248a20438fdfe9fe95c3947)), closes [#1359](https://github.com/acdh-oeaw/apis-core-rdf/issues/1359)
* **relations:** handle overflow in relations dialog ([4b08b6f](https://github.com/acdh-oeaw/apis-core-rdf/commit/4b08b6f0680d0448fee2ce456507101e92069509))
* **relations:** order fields before initializing FormHelper ([c8e9945](https://github.com/acdh-oeaw/apis-core-rdf/commit/c8e9945f0cc0a1b1e347fb04b6779449ae8d4639)), closes [#1355](https://github.com/acdh-oeaw/apis-core-rdf/issues/1355)

## [0.30.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.29.0...v0.30.0) (2024-11-07)


### Features

* **generic:** add a repr dunder method to the GenericModel ([e0b44aa](https://github.com/acdh-oeaw/apis-core-rdf/commit/e0b44aaf151c865c12f8990a3bf55556db32536a))
* **relations:** implement duplicate and merge signal receivers ([77b9f10](https://github.com/acdh-oeaw/apis-core-rdf/commit/77b9f108a5667cabf72cf313c3b30f766df1db1d)), closes [#1251](https://github.com/acdh-oeaw/apis-core-rdf/issues/1251)
* **relations:** new template to list relations ([a6d7030](https://github.com/acdh-oeaw/apis-core-rdf/commit/a6d7030c17d59ee4bf7005c91201f71192ba3abf)), closes [#489](https://github.com/acdh-oeaw/apis-core-rdf/issues/489)
* **relations:** put relations in a block ([65225d0](https://github.com/acdh-oeaw/apis-core-rdf/commit/65225d0e77f61a656ba0352a344113f346d69108))
* **relations:** run autocomplete results through js method ([947fbf4](https://github.com/acdh-oeaw/apis-core-rdf/commit/947fbf411b071ac042c4a8db0955d602510e0a66))
* **relations:** use content type specific autocomplete in relation form ([da939b8](https://github.com/acdh-oeaw/apis-core-rdf/commit/da939b8335786162f951014fd967d8f523dcb36f))
* **sample_project:** automaticall add admin ([32c8f4e](https://github.com/acdh-oeaw/apis-core-rdf/commit/32c8f4eeee2e4bca04d04020746c7872a796f20b)), closes [#1292](https://github.com/acdh-oeaw/apis-core-rdf/issues/1292)
* **sample_project:** tabbed relations for person ([ff675bd](https://github.com/acdh-oeaw/apis-core-rdf/commit/ff675bdc4d8d7a698ee8496b8d43a1873ca4756d))


### Bug Fixes

* **core:** don't underline hovered footer icon links ([20ec314](https://github.com/acdh-oeaw/apis-core-rdf/commit/20ec3148aa351ab5ae2649f2606415cd63c079eb))
* **documentation:** force read lazy objects as str ([a0f52bf](https://github.com/acdh-oeaw/apis-core-rdf/commit/a0f52bf44f65d071ac0be22b3efb9b98b60f1b38)), closes [#1319](https://github.com/acdh-oeaw/apis-core-rdf/issues/1319)

## [0.29.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.28.0...v0.29.0) (2024-10-15)


### ⚠ BREAKING CHANGES

* **apis_metainfo:** drop unused attributes from Uri model

### Features

* **collections:** add constraints to collections ([818e998](https://github.com/acdh-oeaw/apis-core-rdf/commit/818e998935b67ee6396714fe0395f86d6807cdf9))
* **collections:** add custom collection manager ([3e19e49](https://github.com/acdh-oeaw/apis-core-rdf/commit/3e19e49a8e71496fe6000a76843b3cbf6bca71bd))
* **generic:** introduce `default_search_fields` method ([494ee61](https://github.com/acdh-oeaw/apis-core-rdf/commit/494ee618ffaf9575058c05e2c5257deef2022f7a))
* **generic:** introduce MoreLessColumn ([3d8ebc7](https://github.com/acdh-oeaw/apis-core-rdf/commit/3d8ebc7c1e95351bbb08046a3ed4e7561175e445))
* **generic:** use the `default_search_fields` method ([c3ff714](https://github.com/acdh-oeaw/apis-core-rdf/commit/c3ff7147dbf51f485b548386f06079f1ed3d9fa2))
* **generic:** use the `default_search_fields` method ([2279283](https://github.com/acdh-oeaw/apis-core-rdf/commit/22792833e40f98e4f42aa74ac90b862d9d1c7864))
* **relations:** allow more generic relation tables ([6142910](https://github.com/acdh-oeaw/apis-core-rdf/commit/6142910458a58e46cf8ea46f3d70e35a8b3d0260))
* **sample_project:** example for MoreLessColumn ([8b0d40e](https://github.com/acdh-oeaw/apis-core-rdf/commit/8b0d40ea4b44b35d61395739a709eaf65234be98))


### Bug Fixes

* **apis_entities,apis_relations:** move TempTriple update code to signal ([ad25547](https://github.com/acdh-oeaw/apis-core-rdf/commit/ad2554771fa7f660cdfb80c353bf05b0ffed0291)), closes [#1228](https://github.com/acdh-oeaw/apis-core-rdf/issues/1228)
* **apis_entities:** correct merge link ([0088fc6](https://github.com/acdh-oeaw/apis-core-rdf/commit/0088fc6ff4d4b1541c258c23c85a8027b4a3e141)), closes [#1278](https://github.com/acdh-oeaw/apis-core-rdf/issues/1278)
* **apis_relations:** call block.super in the col-one block ([720b637](https://github.com/acdh-oeaw/apis-core-rdf/commit/720b637b4eaf22276ed897962cf5a680dbdee0df))
* **apis_relations:** edit button appearance ([510d0ed](https://github.com/acdh-oeaw/apis-core-rdf/commit/510d0edeaef9cff73205839168bbc835a42eb886))
* **generic:** redirect to detail page after merge ([86d04a3](https://github.com/acdh-oeaw/apis-core-rdf/commit/86d04a35b781cefda075981d00eb453cf43c12bc)), closes [#1282](https://github.com/acdh-oeaw/apis-core-rdf/issues/1282)
* **relations:** use form instead of hardcoding the id ([08abeba](https://github.com/acdh-oeaw/apis-core-rdf/commit/08abebadf6d949b018463c09589a02af5ff51315))
* **relations:** use javascript onclick instead of htmx on:click ([db2b008](https://github.com/acdh-oeaw/apis-core-rdf/commit/db2b008568e6d5854f263a7e8d7e3d7ab2265b46)), closes [#1265](https://github.com/acdh-oeaw/apis-core-rdf/issues/1265)


### Code Refactoring

* **apis_metainfo:** drop unused attributes from Uri model ([5c0156e](https://github.com/acdh-oeaw/apis-core-rdf/commit/5c0156e8444a69eea984a5217586ae94ebb929a9))

## [0.28.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.27.0...v0.28.0) (2024-10-03)


### Features

* **apis_entities:** adapt merge form to use new enrich view ([ba7ad4c](https://github.com/acdh-oeaw/apis-core-rdf/commit/ba7ad4c2b450e83069b960d012ff4e3f544306e8))
* **apis_entities:** add a E21_PersonFromWikidata RDF configuration ([d249d99](https://github.com/acdh-oeaw/apis-core-rdf/commit/d249d9972914152fada5163b9cba9dbb2be95932))
* **apis_entities:** add a link to the enrich uri to all linked URIs ([c0b459d](https://github.com/acdh-oeaw/apis-core-rdf/commit/c0b459d1e0b8af5acdc67b8e0319ba2c666e44bd))
* **apis_entities:** add a util method to get all entity conten types ([0be8476](https://github.com/acdh-oeaw/apis-core-rdf/commit/0be8476979ac8a55c0bc520619d97f771b48e2e3))
* **apis_entities:** drop old version style urls ([2f85686](https://github.com/acdh-oeaw/apis-core-rdf/commit/2f85686947f31ba28e5807b02ee2fc81cedc62cc)), closes [#1196](https://github.com/acdh-oeaw/apis-core-rdf/issues/1196)
* **apis_entities:** introduce a map view for E53_Place entities ([ba68493](https://github.com/acdh-oeaw/apis-core-rdf/commit/ba6849377bc90e81a16ef13fcaa43c9ebebfdf66))
* **core:** add a templatetag that returns the url to the git repo ([82fa96d](https://github.com/acdh-oeaw/apis-core-rdf/commit/82fa96d27557f2d46619c657e14de822a5068b3c)), closes [#1217](https://github.com/acdh-oeaw/apis-core-rdf/issues/1217)
* **core:** allow to skip dateparsing in LegacyDateMixin ([0925fc0](https://github.com/acdh-oeaw/apis-core-rdf/commit/0925fc0c7202c01bfa309ca3db444a48d2f29621)), closes [#1208](https://github.com/acdh-oeaw/apis-core-rdf/issues/1208)
* **core:** introduce templatetag to list fields for a contenttype ([2c02a94](https://github.com/acdh-oeaw/apis-core-rdf/commit/2c02a94118540f8de6fcff2d40b85e42fa8bfa53))
* **documentation:** add a new `apis_core.documentation` app ([5e44520](https://github.com/acdh-oeaw/apis-core-rdf/commit/5e44520c3256207a33393a6219024f194edd92c0))
* **generic:** add a view for enriching entities with external data ([9e8fe5c](https://github.com/acdh-oeaw/apis-core-rdf/commit/9e8fe5cc5c8bf9bde7daf3379d9d9b10727a9e70))
* **generic:** add an import button to the list views ([7c0c5f4](https://github.com/acdh-oeaw/apis-core-rdf/commit/7c0c5f43fba3a09fa535ae70996998cafa020f17)), closes [#1171](https://github.com/acdh-oeaw/apis-core-rdf/issues/1171)
* **generic:** allow to set paginate_by using a table attribute ([1cc3792](https://github.com/acdh-oeaw/apis-core-rdf/commit/1cc379216278672181e08f556bf798182560389d))
* **relations:** replace bootstrap modal with html dialog ([a2e80fa](https://github.com/acdh-oeaw/apis-core-rdf/commit/a2e80fad3fcfc2903067a072de13af4d0406b6e6))
* **sample_project:** enable debug logging ([20ace0e](https://github.com/acdh-oeaw/apis-core-rdf/commit/20ace0e8dc6e13a78680746850e2e47831984df2)), closes [#1252](https://github.com/acdh-oeaw/apis-core-rdf/issues/1252)
* **sample_project:** enable the `apis_core.documentation` app ([48ab3bf](https://github.com/acdh-oeaw/apis-core-rdf/commit/48ab3bfde3ffb0c9dc4a315a010a17113b2ed00a))


### Bug Fixes

* **core:** redirect to root after logout ([b74b6e7](https://github.com/acdh-oeaw/apis-core-rdf/commit/b74b6e76885bf021883f4e7f2eafc4e99b8f7c12))
* **core:** use a generic setting instead of an environment variable ([2eb364d](https://github.com/acdh-oeaw/apis-core-rdf/commit/2eb364d126796f681f89fb8aa6b155861e054744))
* **documentation:** add initial value ([af447ce](https://github.com/acdh-oeaw/apis-core-rdf/commit/af447ceac71c70be31251cdde37d83bc502ff85f))
* **generic:** fix typo logging -&gt; logger ([86ee0a2](https://github.com/acdh-oeaw/apis-core-rdf/commit/86ee0a2a3b9d4210952c3baca31f45fb61c1c532))
* **generic:** reuse `get_model_fields` templatetag in `modeldict` ([9376df7](https://github.com/acdh-oeaw/apis-core-rdf/commit/9376df70705afdf0c382751ea4433a7a1a8a8b12)), closes [#1249](https://github.com/acdh-oeaw/apis-core-rdf/issues/1249)
* **generic:** show verbose name instead of contenttype name in list view ([3232ea6](https://github.com/acdh-oeaw/apis-core-rdf/commit/3232ea6e69ea8ce6a8b8eaed35753a457ec3479e)), closes [#1246](https://github.com/acdh-oeaw/apis-core-rdf/issues/1246)
* **relations:** disable cache on the relation_match_target function ([e9a3111](https://github.com/acdh-oeaw/apis-core-rdf/commit/e9a31116fa6278da038637b89cd6cb1acaa000d5)), closes [#1207](https://github.com/acdh-oeaw/apis-core-rdf/issues/1207)


### Documentation

* **customization:** add documentation regarding paginate_by ([5c4da6f](https://github.com/acdh-oeaw/apis-core-rdf/commit/5c4da6fe32fd76114eaf7eebee42a0b471861332))
* readd the development chapter, that was accidently removed ([005f975](https://github.com/acdh-oeaw/apis-core-rdf/commit/005f975f4712cdc9597fded1ae99a1ad15be717f))
* update development section ([8eb0447](https://github.com/acdh-oeaw/apis-core-rdf/commit/8eb044773b4b620c244329ca516233c5e9067bfc))
* update the CONTRIBUTING file ([e09bc43](https://github.com/acdh-oeaw/apis-core-rdf/commit/e09bc43257a44156686754523f47c4448c0464fd)), closes [#852](https://github.com/acdh-oeaw/apis-core-rdf/issues/852)

## [0.27.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.26.0...v0.27.0) (2024-09-24)


### Features

* **apis_entites:** introduce js and css for showing a popover map ([1e56ad1](https://github.com/acdh-oeaw/apis-core-rdf/commit/1e56ad1865ead6895e517ae0947f9f9d1217c33b))
* **apis_entities:** introduce a e53_place autocomplete template ([ac358a7](https://github.com/acdh-oeaw/apis-core-rdf/commit/ac358a7e7d915e756f2de776d5ba95854bb5bd5e))
* **apis_entities:** introduce a mergeform template tag ([f7c5677](https://github.com/acdh-oeaw/apis-core-rdf/commit/f7c56773bb8d5386bb4eaef4926fcaf0a8fc2ad0))
* **apis_metainfo:** print warning when APIS_BASE_URI is not set ([1727387](https://github.com/acdh-oeaw/apis-core-rdf/commit/1727387fc002726a0f673197659ca371162d2d35))
* **apis_relations:** add missing migrations ([39a1dcd](https://github.com/acdh-oeaw/apis-core-rdf/commit/39a1dcdfbbd47e8ccb4923f50f524b9431225187))
* **generic:** introduce a generic merge view ([5f21c4d](https://github.com/acdh-oeaw/apis-core-rdf/commit/5f21c4dfb1a428ff076006029f6474c569c9fa1a))
* **generic:** refactor the merge logic and move parts to generic ([b0e5294](https://github.com/acdh-oeaw/apis-core-rdf/commit/b0e529494a574775ffd366c43293a2da0f80b129))
* **sample_project:** add missing migrations ([49c21bc](https://github.com/acdh-oeaw/apis-core-rdf/commit/49c21bc37e38b5ba99e9749b9e6a3ba24da28010))


### Bug Fixes

* **apis_entities:** merge - use src obj's bool val ([c73203e](https://github.com/acdh-oeaw/apis-core-rdf/commit/c73203edb04a512b0e0510de6cc8c4aa3f9c8811)), closes [#818](https://github.com/acdh-oeaw/apis-core-rdf/issues/818)
* **apis_entities:** use example.org as fallback and drop global ([217ca90](https://github.com/acdh-oeaw/apis-core-rdf/commit/217ca90e5127d657d23af702d802d0ea5df63537))
* **core:** replace logout link with a logout form ([a8789a6](https://github.com/acdh-oeaw/apis-core-rdf/commit/a8789a6c41c3908651266daf0366b501c5df2934)), closes [#910](https://github.com/acdh-oeaw/apis-core-rdf/issues/910)
* **generic:** fix templatetag loading in merge template ([3812512](https://github.com/acdh-oeaw/apis-core-rdf/commit/3812512ad2f27ec0dc9e54f51dfc933872994942))
* **generic:** remove cache decorator from GenericModelImporter ([5b44c8a](https://github.com/acdh-oeaw/apis-core-rdf/commit/5b44c8aab1c2d09481659690d6ddcaef6b3f7c90)), closes [#1204](https://github.com/acdh-oeaw/apis-core-rdf/issues/1204)
* **relations:** display choices in create form ([bb66d57](https://github.com/acdh-oeaw/apis-core-rdf/commit/bb66d572d5283937ec296a85ba11c0f522db3d1b)), closes [#1193](https://github.com/acdh-oeaw/apis-core-rdf/issues/1193)

## [0.26.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.25.0...v0.26.0) (2024-09-17)


### ⚠ BREAKING CHANGES

* **core:** cleanup the base.html template
* **core:** rename templatetags module to `core`
* **history:** rename templatetags module to `history`
* **generic:** rename templatetags module to `generic`
* **apis_metainfo:** drop `apis_metainfo_extras` templatetag module
* **collections:** rename templatetags module to `collections`
* **apis_entities:** rename templatetags module to `apis_entities`

### Features

* **apis_relations:** use the base template to override relations menu ([5f27f04](https://github.com/acdh-oeaw/apis-core-rdf/commit/5f27f04146228d255a9e46dd53bb36e9947542a2)), closes [#1144](https://github.com/acdh-oeaw/apis-core-rdf/issues/1144)
* **core:** introduce a `footer-left.html` template with API links ([d2d3891](https://github.com/acdh-oeaw/apis-core-rdf/commit/d2d3891462af685acf8375119fe4337aa4100394))
* **generic:** add logging to GenericModelImporter ([8d282cd](https://github.com/acdh-oeaw/apis-core-rdf/commit/8d282cd582a39bd0e970847ccff58d3e5814b87a))


### Bug Fixes

* **apis_metainfo:** drop UriGetOrCreate view and related stuff ([57a7b87](https://github.com/acdh-oeaw/apis-core-rdf/commit/57a7b8769ce007ec9a48173f2c7a67231f403519)), closes [#1135](https://github.com/acdh-oeaw/apis-core-rdf/issues/1135)
* **apis_relations:** drop unused templatetag loading in template ([46b5ac9](https://github.com/acdh-oeaw/apis-core-rdf/commit/46b5ac9ca194f386c6271e5e4afa999162c6039b))
* **core:** readd login.html template that was accidently dropped ([9166e86](https://github.com/acdh-oeaw/apis-core-rdf/commit/9166e86188f5a5197d98a4e86dc08c14533c0fa7))
* **generic:** replace `create` with `add` for required permission ([dc9b42c](https://github.com/acdh-oeaw/apis-core-rdf/commit/dc9b42cca203d0fa31df1daf041f39d10b3075d2)), closes [#1173](https://github.com/acdh-oeaw/apis-core-rdf/issues/1173)
* **generic:** replace custom filterset factory with upstream one ([a4d171b](https://github.com/acdh-oeaw/apis-core-rdf/commit/a4d171b330daa2c3a4fe7af44c1c0cca6e1808e6)), closes [#952](https://github.com/acdh-oeaw/apis-core-rdf/issues/952)
* **generic:** use Serializer as base for SimpleObjectSerializer ([e0eaebb](https://github.com/acdh-oeaw/apis-core-rdf/commit/e0eaebba0a40ef0fee7d65fe4f95c6e9d7141495))
* **relations:** drop the model field from the RelationSerializer ([2f1e549](https://github.com/acdh-oeaw/apis-core-rdf/commit/2f1e5491815e2518d421c692856330d156551985))
* **relations:** set model of RelationSerializer ([9192e97](https://github.com/acdh-oeaw/apis-core-rdf/commit/9192e97653735e8033efb9c1425bbde69c5bed2c)), closes [#1178](https://github.com/acdh-oeaw/apis-core-rdf/issues/1178)
* **utils:** make value detection in get_html_diff more reliable ([eed28c0](https://github.com/acdh-oeaw/apis-core-rdf/commit/eed28c020feaa107aae6fc063d40a19445b822b3))


### Code Refactoring

* **apis_entities:** rename templatetags module to `apis_entities` ([c9fe20f](https://github.com/acdh-oeaw/apis-core-rdf/commit/c9fe20fee4bbfe5708a069a6aeb1652a47aaf662))
* **apis_metainfo:** drop `apis_metainfo_extras` templatetag module ([ed1c38d](https://github.com/acdh-oeaw/apis-core-rdf/commit/ed1c38dff77d2c0951336a00f5dae1c41cbd8bb6))
* **collections:** rename templatetags module to `collections` ([a78bb84](https://github.com/acdh-oeaw/apis-core-rdf/commit/a78bb8494d5a453c275c628e4e5d0c05a546f618))
* **core:** cleanup the base.html template ([f1f7f73](https://github.com/acdh-oeaw/apis-core-rdf/commit/f1f7f7363153fa3507d3eb4df93433aacceda1bf))
* **core:** rename templatetags module to `core` ([3714227](https://github.com/acdh-oeaw/apis-core-rdf/commit/371422755d7ca4028bf24a763cae93477eac12db))
* **generic:** rename templatetags module to `generic` ([1d9c159](https://github.com/acdh-oeaw/apis-core-rdf/commit/1d9c15912f104f030e3c2a9d2534870aea397a9e))
* **history:** rename templatetags module to `history` ([ffa1d14](https://github.com/acdh-oeaw/apis-core-rdf/commit/ffa1d14244ab912e3671ea6b1e13dc17a83c231d))

## [0.25.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.24.0...v0.25.0) (2024-09-06)


### Features

* **apis_entites:** add a generic entites autocomplete endpoint ([c1a76e0](https://github.com/acdh-oeaw/apis-core-rdf/commit/c1a76e09fbcc9ff49e5a205372fd11c140fc2604))
* **collections:** allow add all changes in a session to a collection ([27f7e8d](https://github.com/acdh-oeaw/apis-core-rdf/commit/27f7e8d2300fe819508bd992293d5d84376dcbfc)), closes [#1066](https://github.com/acdh-oeaw/apis-core-rdf/issues/1066)
* **collections:** introduce custom collections table ([fd250c7](https://github.com/acdh-oeaw/apis-core-rdf/commit/fd250c7f52a3703b8d222481eef557bc1aaf029e))
* **generic:** add `import_into_instance` method to GenericModelImporter ([2e12b76](https://github.com/acdh-oeaw/apis-core-rdf/commit/2e12b7665d4ad717958e3d9f3a03d61caddc4fbf))
* **generic:** add caching to GenericModelImporter ([b20fd4e](https://github.com/acdh-oeaw/apis-core-rdf/commit/b20fd4e5d5cd4b34cdc237bfad6e65f7932b4104))
* **generic:** add the number of objects to the buttons in the overview ([a48d172](https://github.com/acdh-oeaw/apis-core-rdf/commit/a48d172b23bc3325e9e873496b0d04517363b36a))
* **generic:** introduce a `get_attribute` templatetag ([8654d1b](https://github.com/acdh-oeaw/apis-core-rdf/commit/8654d1bcd0ddcc0c55cb3a70cdc40bb20fb8e56f))
* **generic:** introduce filter that counts contenttype instances ([052f8de](https://github.com/acdh-oeaw/apis-core-rdf/commit/052f8deb69a01a119e31e4d14bc74dc7e2763d74))
* **generic:** introduce SimpleObjectSerializer ([d03be68](https://github.com/acdh-oeaw/apis-core-rdf/commit/d03be688131a6ac50ca8ed3a4f12b74155bf8831))
* **history:** add ng relations to history view ([36b02ab](https://github.com/acdh-oeaw/apis-core-rdf/commit/36b02ab13c8e2d663420f9c47df67fc81729433e)), closes [#1112](https://github.com/acdh-oeaw/apis-core-rdf/issues/1112)
* **relations:** add a relations_verbose_name_listview_url templatetag ([3e39858](https://github.com/acdh-oeaw/apis-core-rdf/commit/3e398589f5c3ea1c7d8d776d9379df7965591449))
* **relations:** allow to specify obj or subj types using natural keys ([c0d92f8](https://github.com/acdh-oeaw/apis-core-rdf/commit/c0d92f8ecbef53edd2acc09eb9ccbf9661d8dd76))
* **relations:** extend the base template to include relation menu items ([74feebb](https://github.com/acdh-oeaw/apis-core-rdf/commit/74feebb9ed5276e4355fb4ea47d60ed4ecbd066d)), closes [#1083](https://github.com/acdh-oeaw/apis-core-rdf/issues/1083)
* **relations:** introduce get_all_relation_subj_and_obj helper function ([ed19960](https://github.com/acdh-oeaw/apis-core-rdf/commit/ed19960c9cba87da9d2c9a3ce1d86bf7d1939143))
* **relations:** introduce new relations implementation ([1799ea6](https://github.com/acdh-oeaw/apis-core-rdf/commit/1799ea63c3c222c075a2006495675dbdc7651315))
* **relations:** override default queryset to include subclasses ([7ef2959](https://github.com/acdh-oeaw/apis-core-rdf/commit/7ef29594c89f39371636de487f6dc0a503125951))
* **relations:** override the default filterset for relations ([1f908de](https://github.com/acdh-oeaw/apis-core-rdf/commit/1f908dea0afd2363dfba936dc03870696290cd0b))
* **relations:** override the default serializer for relations ([9bb30c3](https://github.com/acdh-oeaw/apis-core-rdf/commit/9bb30c3ffd63a25f7f1cacb6fba653595047735e))
* **relations:** override the viewset queryset to include subclasses ([2378dce](https://github.com/acdh-oeaw/apis-core-rdf/commit/2378dcec97636fd00018874426f5c2c0bf311178))


### Bug Fixes

* **apis_entities:** make autocomplete work with multilevel inheritance ([50a2af1](https://github.com/acdh-oeaw/apis-core-rdf/commit/50a2af19d6739a08c4db9a0fac4ff17b5f6c9133)), closes [#1109](https://github.com/acdh-oeaw/apis-core-rdf/issues/1109)
* **apis_relations:** fix relations table date render method ([3f41633](https://github.com/acdh-oeaw/apis-core-rdf/commit/3f41633dab2f09aeae6a4e84d3e6dbf22420863c))
* **collections:** fix typo in template url argument ([8559c49](https://github.com/acdh-oeaw/apis-core-rdf/commit/8559c4947948e890c9694a09eeaf5110bed96b27))
* **collections:** use an app_name and include urls in apis_core.urls ([1c70aa5](https://github.com/acdh-oeaw/apis-core-rdf/commit/1c70aa5ea6ffc27c3369c0bbf2a80da431a17589))
* **history:** change column name in table to a more accurate term ([368b19c](https://github.com/acdh-oeaw/apis-core-rdf/commit/368b19ce0857d99db55cb65056415e948f806342)), closes [#878](https://github.com/acdh-oeaw/apis-core-rdf/issues/878)
* **history:** remove verbose name from APISHistoricalRecord ([0c62e85](https://github.com/acdh-oeaw/apis-core-rdf/commit/0c62e850d7403e98e59a1601efc1261cdc8e69b8)), closes [#920](https://github.com/acdh-oeaw/apis-core-rdf/issues/920)
* **relations:** make `get_relation_targets_from` method more targeted ([35b6709](https://github.com/acdh-oeaw/apis-core-rdf/commit/35b670918d42148d2fe99b940d0895998b4e6efa))
* **sample_project:** move generic and core to end of INSTALLED_APPS ([d029ed3](https://github.com/acdh-oeaw/apis-core-rdf/commit/d029ed3abf46c27b657be88e132b89b382b7ac45))
* **sample_project:** set the string repr for the Profession model ([9c4a87e](https://github.com/acdh-oeaw/apis-core-rdf/commit/9c4a87eb2108f52de264a68dbfb7917a843c7791))
* **sample_project:** show password only if passwordfile exists ([b9aa308](https://github.com/acdh-oeaw/apis-core-rdf/commit/b9aa30825f89af0ff0183fe29eabb2aa7d04b580))


### Documentation

* **collections:** add documentation about new session toggle ([bdfde27](https://github.com/acdh-oeaw/apis-core-rdf/commit/bdfde27d1a1f94bac2d7e411d0cf14056c4ab073))
* **ontology:** update ontology docs regarding the natural key notation ([d205399](https://github.com/acdh-oeaw/apis-core-rdf/commit/d2053993c1217c726b1479aad394bc5322859bc3))
* **relations:** add documentation about Relations to ontology chapter ([7f16ace](https://github.com/acdh-oeaw/apis-core-rdf/commit/7f16ace3c1f01063f20665823a4ff01e25913a7c))

## [0.24.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.23.2...v0.24.0) (2024-08-13)


### ⚠ BREAKING CHANGES

* **utils:** drop `filtermethods`

### Features

* **apis_entities:** add `changed since` filter to entity filterset ([fde59c7](https://github.com/acdh-oeaw/apis-core-rdf/commit/fde59c777a2888ef7037506d2148a6766ca19f68)), closes [#335](https://github.com/acdh-oeaw/apis-core-rdf/issues/335)
* **apis_entities:** add a default search field to the entity filtersets ([7cd7906](https://github.com/acdh-oeaw/apis-core-rdf/commit/7cd79063d763a1f91c28a0b77feced219b209213))
* **apis_entities:** add external Uris to detail view ([69fe3ba](https://github.com/acdh-oeaw/apis-core-rdf/commit/69fe3ba581291f6c4acd44bfd48a22248116b238)), closes [#861](https://github.com/acdh-oeaw/apis-core-rdf/issues/861)


### Bug Fixes

* **apis_entities:** fix sparql queries for abstract base classes ([6ac2373](https://github.com/acdh-oeaw/apis-core-rdf/commit/6ac23730d13fe7c40726db15d5206a8fd8b29730))
* **apis_entities:** set return type of serializer method ([900eb3a](https://github.com/acdh-oeaw/apis-core-rdf/commit/900eb3a0fa4e389f03ee526cd84abeec21f633d5))
* **history:** set return types of serialzers methods ([667503a](https://github.com/acdh-oeaw/apis-core-rdf/commit/667503adcdfba96e733e0802d15bbde3f4e301d8))
* **sample_project:** add autocomplete querysets for person and place ([8d6d8dd](https://github.com/acdh-oeaw/apis-core-rdf/commit/8d6d8ddcd5c7def101b471d13f767e2ccf90bfaf)), closes [#900](https://github.com/acdh-oeaw/apis-core-rdf/issues/900)


### Documentation

* add anker to README to allow for partial include in docs ([e0bbaa6](https://github.com/acdh-oeaw/apis-core-rdf/commit/e0bbaa68cf347768b5a58798980a66294f0aa26d)), closes [#1075](https://github.com/acdh-oeaw/apis-core-rdf/issues/1075)
* add section `ontology` and describe how to add entities ([0603e34](https://github.com/acdh-oeaw/apis-core-rdf/commit/0603e3442668e7520cfa3b08d8fb042c9c986ebe))
* improve configuration chapter ([7e24ec2](https://github.com/acdh-oeaw/apis-core-rdf/commit/7e24ec276afed46f4290145ae8189e8dee3dea4d))
* improve customization chapter ([adb1eb0](https://github.com/acdh-oeaw/apis-core-rdf/commit/adb1eb0bb335d244d1a720f6373f6e1f934addf7))
* improve glossary chapter ([356f3db](https://github.com/acdh-oeaw/apis-core-rdf/commit/356f3db8ea9fb8a854bf67a31781080726a573bd))
* improve installation chapter of the docs ([454090a](https://github.com/acdh-oeaw/apis-core-rdf/commit/454090aa317d18828902812034b366b33488ef31))
* move history and collections features to dedicated page ([4d8c1f2](https://github.com/acdh-oeaw/apis-core-rdf/commit/4d8c1f2fbc70d5d93ef2b38455d0825d610de65a))
* remove not used and outdated doc sections ([5b107cc](https://github.com/acdh-oeaw/apis-core-rdf/commit/5b107cc08732ca78c6ea2f55e126f3c2b23f2706))
* remove not used entries from index.rst ([e348c53](https://github.com/acdh-oeaw/apis-core-rdf/commit/e348c53b10dc7ca6174add7529f87e63dc24fc96))
* reuse the pyproject metadata in sphinx docs ([e8de605](https://github.com/acdh-oeaw/apis-core-rdf/commit/e8de6050c65c0b720ff618eea795aad94abb8e27))


### Code Refactoring

* **utils:** drop `filtermethods` ([032c1be](https://github.com/acdh-oeaw/apis-core-rdf/commit/032c1be425fbc0afef1fb345dd1e76102e2de303)), closes [#790](https://github.com/acdh-oeaw/apis-core-rdf/issues/790)

## [0.23.2](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.23.1...v0.23.2) (2024-07-03)


### Bug Fixes

* **apis_entities:** remove inherited related fields from column list ([44a983d](https://github.com/acdh-oeaw/apis-core-rdf/commit/44a983de4a07d629dc31c3443e87fa9ba5257ce5)), closes [#1029](https://github.com/acdh-oeaw/apis-core-rdf/issues/1029)
* **core:** add schema information to the dumpdata api endpoint ([e622977](https://github.com/acdh-oeaw/apis-core-rdf/commit/e62297774a97efcc0e445fb627b25df503240fc5))
* **generic:** ModelViewSet: check if renderer exists before using it ([dd21e84](https://github.com/acdh-oeaw/apis-core-rdf/commit/dd21e84b1bb7ff28349b5e0354b51148b158b283))

## [0.23.1](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.23.0...v0.23.1) (2024-07-02)


### Bug Fixes

* **generic:** include ManyToManyFields in list view ([2763e0e](https://github.com/acdh-oeaw/apis-core-rdf/commit/2763e0e77ad60feea233c6a57a918528d2516cbb)), closes [#1020](https://github.com/acdh-oeaw/apis-core-rdf/issues/1020)
* **generic:** repair table columns ordering ([6762a17](https://github.com/acdh-oeaw/apis-core-rdf/commit/6762a175ae87fb9b1b592a5f47c7406c81b3ad52)), closes [#1022](https://github.com/acdh-oeaw/apis-core-rdf/issues/1022)

## [0.23.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.22.0...v0.23.0) (2024-07-01)


### ⚠ BREAKING CHANGES

* **generic:** rename `GenericImporter` to `GenericModelImporter`

### Features

* **generic:** add data received to importer error message ([9570bbd](https://github.com/acdh-oeaw/apis-core-rdf/commit/9570bbddb9a9844abc6c99a457074c61bce66572))
* **generic:** allow apiview to use custom serializers ([0bcd61b](https://github.com/acdh-oeaw/apis-core-rdf/commit/0bcd61bc29cc9c571a3b01319477b5a80bb54f48))
* **generic:** allow to set default search fields in the model ([763a866](https://github.com/acdh-oeaw/apis-core-rdf/commit/763a86600936bc3e5d7719110ca9167e76aedbf4))
* **generic:** fix and extend the columns selector ([eaef405](https://github.com/acdh-oeaw/apis-core-rdf/commit/eaef4055b60accbf4c691cf9a2642cf47989af40)), closes [#735](https://github.com/acdh-oeaw/apis-core-rdf/issues/735)
* **generic:** let the importer try rdf before the json fallback ([97dba9d](https://github.com/acdh-oeaw/apis-core-rdf/commit/97dba9d82310e94bea789b9313ab460808891bc1))
* **generic:** make importer return a message on error ([c60ad36](https://github.com/acdh-oeaw/apis-core-rdf/commit/c60ad36a732403893bc1d1dd432e71bfde8bf341))
* **generic:** ship generic RDF renderers ([b60a0e5](https://github.com/acdh-oeaw/apis-core-rdf/commit/b60a0e5ac7d86186eb4e8cf2b533e4dc69fb9d04))


### Bug Fixes

* **apis_entities:** let EntityToContenttypeConverter handle ContentType ([16534ad](https://github.com/acdh-oeaw/apis-core-rdf/commit/16534add460c4c9a2936f5de8a6f9cbe62bdebeb))
* **apis_entities:** only list possible properties in filterset form ([a156cb4](https://github.com/acdh-oeaw/apis-core-rdf/commit/a156cb45921b1025300e84e1a3ec114b38be0c0f)), closes [#949](https://github.com/acdh-oeaw/apis-core-rdf/issues/949)
* **apis_entities:** split excluded filters and excluded columns ([d8649d7](https://github.com/acdh-oeaw/apis-core-rdf/commit/d8649d7d907d07f2ef6b3e0def374d52645d46cc))
* **apis_relations:** make relation edit link change color on hover ([bbdf4c7](https://github.com/acdh-oeaw/apis-core-rdf/commit/bbdf4c7c538ca1ca81e45abe5a55ab3ca7e807ec))
* **core:** add version to base template if debug is turned on ([c8f293e](https://github.com/acdh-oeaw/apis-core-rdf/commit/c8f293e45d8eab2c661a602836dc93051700e571)), closes [#981](https://github.com/acdh-oeaw/apis-core-rdf/issues/981)
* **utils:** add a margin class to the NewlineSeparatedListField's widget ([59c4402](https://github.com/acdh-oeaw/apis-core-rdf/commit/59c44023494a40aadd432b2f96d64b4f616465f8))
* **utils:** create_object_from_uri: raise error if no importer found ([89b119a](https://github.com/acdh-oeaw/apis-core-rdf/commit/89b119a71caa423da2dfbc89149d40a0a5a10f41))


### Performance Improvements

* **apis_entities:** refactor and cache the prev and next url methods ([c7ae953](https://github.com/acdh-oeaw/apis-core-rdf/commit/c7ae9530a228b607cfff3b7a29cdf0b9ab0669c4))


### Code Refactoring

* **generic:** rename `GenericImporter` to `GenericModelImporter` ([2784acb](https://github.com/acdh-oeaw/apis-core-rdf/commit/2784acb16b494c45773f45365c311b958b27656e))

## [0.22.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.21.0...v0.22.0) (2024-06-25)


### ⚠ BREAKING CHANGES

* **utils:** drop caching module

### Features

* **apis_entities:** add info message to duplicated object ([77a50fa](https://github.com/acdh-oeaw/apis-core-rdf/commit/77a50fa4aa5de093dce85fbf4dee694ce73c5276)), closes [#893](https://github.com/acdh-oeaw/apis-core-rdf/issues/893)
* **generic:** list all generic models on overview page ([eb53743](https://github.com/acdh-oeaw/apis-core-rdf/commit/eb53743decd2cac8a1363ee312f291803f8bccc9)), closes [#912](https://github.com/acdh-oeaw/apis-core-rdf/issues/912)


### Bug Fixes

* **apis_metainfo:** add missing import ([a4ecc61](https://github.com/acdh-oeaw/apis-core-rdf/commit/a4ecc617babc94f7cd49c62a22caf87f4b8aa1e3))
* **apis_metainfo:** handle unique fields in the duplication logic ([3e66876](https://github.com/acdh-oeaw/apis-core-rdf/commit/3e66876786f64427e86b147206d32b43c10ceca8))
* **apis_metainfo:** make entity_type orderable in the UriTable ([02452ec](https://github.com/acdh-oeaw/apis-core-rdf/commit/02452ec838aba95b49ac091dcce0e47e519c9a51)), closes [#874](https://github.com/acdh-oeaw/apis-core-rdf/issues/874)
* **apis_relations:** replace LinkColumn with Column in TripleTables ([2bdd812](https://github.com/acdh-oeaw/apis-core-rdf/commit/2bdd81249060b373e015f7a804a4f1eb8da8537a)), closes [#676](https://github.com/acdh-oeaw/apis-core-rdf/issues/676)
* **docs:** add documentation regarding GetEntityGeneric ([d883896](https://github.com/acdh-oeaw/apis-core-rdf/commit/d883896b5cfd6b983c7fc342bfeecd96ac8267ce)), closes [#381](https://github.com/acdh-oeaw/apis-core-rdf/issues/381)
* **docs:** fix underline to make sphinx happy ([2a05361](https://github.com/acdh-oeaw/apis-core-rdf/commit/2a0536187cbc539023480f6acfa3dc9acb791363))
* **docs:** remove migrations from the exclude_patterns ([75be82a](https://github.com/acdh-oeaw/apis-core-rdf/commit/75be82a262de55efbe6744eacb9111ae9f0e7335))
* **docs:** repair some docstring formatting issues ([fa88195](https://github.com/acdh-oeaw/apis-core-rdf/commit/fa8819595e2e35360656ba2a7d21d168989897ef))
* **docs:** replace broken README.rst include with README.md ([719931c](https://github.com/acdh-oeaw/apis-core-rdf/commit/719931c8688ba303cd8de5956cd6f219fe563708))
* **docs:** set the language to make sphinx happy ([761367b](https://github.com/acdh-oeaw/apis-core-rdf/commit/761367bd5f9d1953d8029696e503a9fd521195de))
* **sample_project:** fix countdown ([31b05b0](https://github.com/acdh-oeaw/apis-core-rdf/commit/31b05b0d26466d85d456da7da816370038261325)), closes [#992](https://github.com/acdh-oeaw/apis-core-rdf/issues/992)
* **sample_project:** show countdown until redeployment ([f061b0a](https://github.com/acdh-oeaw/apis-core-rdf/commit/f061b0a1f7e649f9440095da60ce915cb7b60bab)), closes [#976](https://github.com/acdh-oeaw/apis-core-rdf/issues/976)
* **utils:** drop caching module ([04f1c9f](https://github.com/acdh-oeaw/apis-core-rdf/commit/04f1c9f7ed214176d235ad23789dad1947e82b00)), closes [#884](https://github.com/acdh-oeaw/apis-core-rdf/issues/884)

## [0.21.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.20.1...v0.21.0) (2024-06-20)


### Features

* **apis_core:** use CustomDefaultRouter instead of DRF DefaultRouter ([9ced7a7](https://github.com/acdh-oeaw/apis-core-rdf/commit/9ced7a78d1d9ff8e9a713a07c319ecbc012a7b81))
* **apis_entities:** introduce CustomSearchFilter and use it ([5c40bc0](https://github.com/acdh-oeaw/apis-core-rdf/commit/5c40bc0ddf9dbffc30bc483dcbd7c2c1ac830929)), closes [#855](https://github.com/acdh-oeaw/apis-core-rdf/issues/855)
* **generic:** add CustomAPIRootView & CustomDefaultRouter ([d0428f0](https://github.com/acdh-oeaw/apis-core-rdf/commit/d0428f0c1719c0e7393a6c40f2dcc36bb58c07ce)), closes [#836](https://github.com/acdh-oeaw/apis-core-rdf/issues/836)
* **generic:** allow passing a prefix to `generate_search_filter` ([335bb75](https://github.com/acdh-oeaw/apis-core-rdf/commit/335bb756d8edf801f7f1c42e1ea43a485a0e2b52))
* **sample_project:** add password to login page ([0be54d2](https://github.com/acdh-oeaw/apis-core-rdf/commit/0be54d2e52c320962d4d2f6f2dceef4127daae9b))
* **sample_project:** provide discworld sample data ([b1bb01f](https://github.com/acdh-oeaw/apis-core-rdf/commit/b1bb01f4600c19d3c86aee729f081a6d8911a769))
* **utils:** add a NewlineSeparatedListField ([6211dc7](https://github.com/acdh-oeaw/apis-core-rdf/commit/6211dc73c90ce0933feaf283a2166aae6b0a0bf6))


### Bug Fixes

* **api:** move `/entities` endpoint to `/api/entities` ([638bc1b](https://github.com/acdh-oeaw/apis-core-rdf/commit/638bc1bbeeb4b0926938a7d43ec78a08ce1f91de))
* **apis_entities:** implement correct related entity query ([13a8a08](https://github.com/acdh-oeaw/apis-core-rdf/commit/13a8a0861c864c0939832eab734d4f2f47f9fb3a)), closes [#943](https://github.com/acdh-oeaw/apis-core-rdf/issues/943)
* **apis_entities:** trigger htmx process after form reloading ([7118205](https://github.com/acdh-oeaw/apis-core-rdf/commit/7118205e3edaa4451f6ad3bfbcc92572379b3159))
* **apis_relations:** respect pagination setting in form table ([1e1c028](https://github.com/acdh-oeaw/apis-core-rdf/commit/1e1c0283de5b7d154ac22f4b0d0b3235116cae76))
* **apis_vocabularies:** remove collections from migrations ([a72e6cd](https://github.com/acdh-oeaw/apis-core-rdf/commit/a72e6cdcf48db50ea2b36f44e566eb1af31c1a05))
* **ci:** replace workflow_call with workflow_dispatch ([5ecf426](https://github.com/acdh-oeaw/apis-core-rdf/commit/5ecf4267879919983396a7dfdba037ce5e6dd072))
* deactivate simple_history plugin for loaddata ([4f5742f](https://github.com/acdh-oeaw/apis-core-rdf/commit/4f5742f4bdebcd5305c0c3b9a3468d8909449631))
* drop `apis` namespace for all url resolvers ([24f91f1](https://github.com/acdh-oeaw/apis-core-rdf/commit/24f91f1ae3e8f88a7cfbffcbc21de16e34246b97)), closes [#876](https://github.com/acdh-oeaw/apis-core-rdf/issues/876)
* **generic:** let ContenttypeConverter also handle string arguments ([2d67cbe](https://github.com/acdh-oeaw/apis-core-rdf/commit/2d67cbe4c14681563714b6a34f81a0bad78816d8))
* **readme:** clean up installation instructions ([5c6ad82](https://github.com/acdh-oeaw/apis-core-rdf/commit/5c6ad8272f8b42245cdaafa9887c3c3da439f4c5))
* **sample_project:** allow all hosts ([37dd165](https://github.com/acdh-oeaw/apis-core-rdf/commit/37dd16529cd1781ef9ff8491a7e5a0f8ec167051))
* **sample_project:** listen on port 5000 by default ([ec10764](https://github.com/acdh-oeaw/apis-core-rdf/commit/ec107644dcf8a9d3b9769a71ba647a3b917bcf50))
* **sample_project:** move app to beginning of INSTALLED_APPS ([7ce3a05](https://github.com/acdh-oeaw/apis-core-rdf/commit/7ce3a0595a077ae2e99d6e386fb23d69444b5b62))
* **sample_project:** show credentials only if not logged in ([d83a68f](https://github.com/acdh-oeaw/apis-core-rdf/commit/d83a68f18b5d6f4bd43e75b9a629e3848c3621da))
* **sample_project:** use environment variables for Django settings ([7ddd8f2](https://github.com/acdh-oeaw/apis-core-rdf/commit/7ddd8f2b22073a02ae098c754ec26a826d83e117))
* use loaddata specific settings in the entrypoint ([5cc2172](https://github.com/acdh-oeaw/apis-core-rdf/commit/5cc21728d79a64fcf1803a812f14f971b239a957))


### Documentation

* include `sample_project` configs instead duplicating them ([571b52e](https://github.com/acdh-oeaw/apis-core-rdf/commit/571b52e8bdabcad071e9a2e35e8d61808771a3f0))
* **sample_project:** add comments to the sample projects settings ([9a7be81](https://github.com/acdh-oeaw/apis-core-rdf/commit/9a7be81a4eb80e6fa3c83cab2c3686a3958aded1))

## [0.20.1](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.20.0...v0.20.1) (2024-06-11)


### Bug Fixes

* **apis_relations:** pass the request to the table ([1340968](https://github.com/acdh-oeaw/apis-core-rdf/commit/13409683bb3e6d6bc742b81921b2bb82024cf4a8))
* **apis_relations:** set default fields ([0f89e92](https://github.com/acdh-oeaw/apis-core-rdf/commit/0f89e9213c53113d7fcedb5871e05c94645e8d1c))
* **generic:** use request intead of context for checking user ([b74158e](https://github.com/acdh-oeaw/apis-core-rdf/commit/b74158e816049d24a259710d7b52fa760526692d))

## [0.20.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.19.1...v0.20.0) (2024-06-11)


### ⚠ BREAKING CHANGES

* **apis_entities:** drop GenericNetworkEntitiesAutocomplete
* **apis_entities:** drop obsolete templatetag

### Features

* add Docker image + sample_project entrypoint & setup ([7a5d265](https://github.com/acdh-oeaw/apis-core-rdf/commit/7a5d26559d9f9ba2ed586b8cc19e7ce6af2dbdf8))
* **apis_entities:** add string methods to abstract base entities ([3f6cb9c](https://github.com/acdh-oeaw/apis-core-rdf/commit/3f6cb9c59c7f8e735bb92ee52471fabeeaaa6083))
* **core:** use django messages framework in base template ([9fd8080](https://github.com/acdh-oeaw/apis-core-rdf/commit/9fd8080598bd89b00220b7406c678f04e1cca5b4))
* **sample_project:** enable bootstrap4 table theme ([ced59f4](https://github.com/acdh-oeaw/apis-core-rdf/commit/ced59f45704b146d4a512bdef53c6b3df7c3f0f7))


### Bug Fixes

* **apis_entities:** allow to skip default uri creation ([8332a3d](https://github.com/acdh-oeaw/apis-core-rdf/commit/8332a3d0bd48b1afc3f202f802f7373d4a79d447)), closes [#436](https://github.com/acdh-oeaw/apis-core-rdf/issues/436)
* **apis_relations, apis_entities:** use `lower` when comparing modelname ([db10fcb](https://github.com/acdh-oeaw/apis-core-rdf/commit/db10fcbc10b986846c3b2b86c174a16ff233ecac))
* **apis_relations,apis_entities:** replace get_object_or_404 ([6785b80](https://github.com/acdh-oeaw/apis-core-rdf/commit/6785b802f3de88d2cd6d7202bbd88cf9320e1bed))
* **core:** don't cache the possible relation entities ([8055f7b](https://github.com/acdh-oeaw/apis-core-rdf/commit/8055f7bcd07ac8de4aac14879c24caa7a048ad4b)), closes [#914](https://github.com/acdh-oeaw/apis-core-rdf/issues/914)
* **sample_project:** add apis_override_select2js to INSTALLED_APPS ([dce75d9](https://github.com/acdh-oeaw/apis-core-rdf/commit/dce75d90793d14f2443cd3f59cd758c7b1487a1c))


### Documentation

* fix formatting issues in history documentation ([111abd4](https://github.com/acdh-oeaw/apis-core-rdf/commit/111abd4f51cd64d9b72a85615c475a744b04edcb)), closes [#843](https://github.com/acdh-oeaw/apis-core-rdf/issues/843)


### Miscellaneous Chores

* **apis_entities:** drop obsolete templatetag ([9e7965d](https://github.com/acdh-oeaw/apis-core-rdf/commit/9e7965d76dd857ea61d7532a05699b9eb7a37213))


### Code Refactoring

* **apis_entities:** drop GenericNetworkEntitiesAutocomplete ([c471255](https://github.com/acdh-oeaw/apis-core-rdf/commit/c471255fb8415dc2d910a4ea4b31ed79b2936136))

## [0.19.1](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.19.0...v0.19.1) (2024-06-05)


### Bug Fixes

* **apis_entities:** fix typo in template (duplciate -&gt; duplicate) ([08f6904](https://github.com/acdh-oeaw/apis-core-rdf/commit/08f690435822074d373407f62fef9941703b3c5c))
* **apis_entities:** remove None values before checking model_class ([05fca69](https://github.com/acdh-oeaw/apis-core-rdf/commit/05fca69c629ad9c2614f8149cc772614a6e56435))
* **apis_metainfo:** fix object duplication ([b8e0e81](https://github.com/acdh-oeaw/apis-core-rdf/commit/b8e0e81fa60d95f17633801df4e7e95e08828c70)), closes [#889](https://github.com/acdh-oeaw/apis-core-rdf/issues/889)
* **sample_project:** move apis root to / and include auth & admin urls ([b1383a6](https://github.com/acdh-oeaw/apis-core-rdf/commit/b1383a69f54af5d556c8ed607ed449f67370b066))

## [0.19.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.18.1...v0.19.0) (2024-06-04)


### ⚠ BREAKING CHANGES

* **core:** drop libre franklin font
* drop old api views
* **apis_metainfo:** drop Collection model

### Features

* **apis_entities:** add endpoint that lists all entities ([6d77a9d](https://github.com/acdh-oeaw/apis-core-rdf/commit/6d77a9d59225a152f7a0c1e773afaadb186c68e5)), closes [#850](https://github.com/acdh-oeaw/apis-core-rdf/issues/850)
* **generic:** add getter for api detail endpoint ([3c80aef](https://github.com/acdh-oeaw/apis-core-rdf/commit/3c80aefefbab436ee294cbc0d6b27f9aa8176df2))
* **generic:** introduce success_url getters for create and update ([eb870f5](https://github.com/acdh-oeaw/apis-core-rdf/commit/eb870f57ae62cefddcc6f23b48d031c244e605d7)), closes [#834](https://github.com/acdh-oeaw/apis-core-rdf/issues/834)
* **generic:** make the form template title differ between create & edit ([ca6d8ef](https://github.com/acdh-oeaw/apis-core-rdf/commit/ca6d8efb24febbb7eed59e90efaa7a450c774804))


### Bug Fixes

* **apis_entities,core:** add templatetag for generating entitymenu ([481ded5](https://github.com/acdh-oeaw/apis-core-rdf/commit/481ded530e6ac06bdf0ea9ad7c3c56b3e15cf669)), closes [#860](https://github.com/acdh-oeaw/apis-core-rdf/issues/860)
* **apis_entities:** set max_length for charfields in abstract classes ([6f7c3dc](https://github.com/acdh-oeaw/apis-core-rdf/commit/6f7c3dc52f64b31550fa3e679a975dbb45cc41eb))
* **docs:** update settings file of doc config ([9774af2](https://github.com/acdh-oeaw/apis-core-rdf/commit/9774af2105c3e91b5e11e890eabb99b1df12a804))
* **generic:** also add detail views to enumarated api_endpoints ([302b18e](https://github.com/acdh-oeaw/apis-core-rdf/commit/302b18e342872cc073eecac3969008a787be3871))
* **history:** returning triples makes only sense for RootObjects ([b292d97](https://github.com/acdh-oeaw/apis-core-rdf/commit/b292d97a61ed2ccc2b84805cb8d90cdcbecf3423))
* **sample_project:** add missing settings and provide urlconf wrapper ([782b5c8](https://github.com/acdh-oeaw/apis-core-rdf/commit/782b5c873da784b8d51eee0d32199d6b427c7e1d))


### Documentation

* add information about the custom schema generator setting ([3278ea1](https://github.com/acdh-oeaw/apis-core-rdf/commit/3278ea1a2a18b042a248181cec0a6c97be33bcc1))
* Add test coverage information to documentation subfolder ([f6767d4](https://github.com/acdh-oeaw/apis-core-rdf/commit/f6767d4b3f0fe71ec3b68205951b28e0c2c93df3))


### Code Refactoring

* **apis_metainfo:** drop Collection model ([7a9aaf2](https://github.com/acdh-oeaw/apis-core-rdf/commit/7a9aaf2e114bc95546670c383b073ff11b54f234)), closes [#576](https://github.com/acdh-oeaw/apis-core-rdf/issues/576)
* **core:** drop libre franklin font ([77929e3](https://github.com/acdh-oeaw/apis-core-rdf/commit/77929e34ea338685a1433b50fe58174d6c043cd9))
* drop old api views ([8da1372](https://github.com/acdh-oeaw/apis-core-rdf/commit/8da1372b031279e4aa054c4f87d223b156d1b8e3))

## [0.18.1](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.18.0...v0.18.1) (2024-05-13)


### Bug Fixes

* **apis_entities:** remove self from list of entities to merge with ([a4fdd63](https://github.com/acdh-oeaw/apis-core-rdf/commit/a4fdd634c0550541698c0e91ba7e0e7908cd5d86))
* **core:** use the capfirst filter on entity menu entries ([4587783](https://github.com/acdh-oeaw/apis-core-rdf/commit/458778354a70a6836ab42a742b2e38f787391824)), closes [#799](https://github.com/acdh-oeaw/apis-core-rdf/issues/799)
* **history:** implement history_date fallback directly in property ([fed77c8](https://github.com/acdh-oeaw/apis-core-rdf/commit/fed77c896e32d5bcc29a1bdef4a00ab68cd3c57d))

## [0.18.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.17.3...v0.18.0) (2024-05-07)


### Features

* **utils:** introduce `get_html_diff` helper ([4af4a60](https://github.com/acdh-oeaw/apis-core-rdf/commit/4af4a60c468a77b29f4deaacb15313d8566febbf))


### Bug Fixes

* **apis_entities:** fix wording of history links ([fd8f6d9](https://github.com/acdh-oeaw/apis-core-rdf/commit/fd8f6d994751ee72db9e64d154fb514d94b8d4a1))
* **apis_entities:** use generic search filter for related entity search ([aa8515f](https://github.com/acdh-oeaw/apis-core-rdf/commit/aa8515fee79786bcaf7894588cfe40bd2d6cef0f))
* **apis_relations:** catch missing RootObject in relation representation ([b9f277c](https://github.com/acdh-oeaw/apis-core-rdf/commit/b9f277ce779e523469942bed32bd4bf7557504d8))
* **history:** add a get_absolute_url method to APISHistoryTableBase ([dc8eec5](https://github.com/acdh-oeaw/apis-core-rdf/commit/dc8eec5d1e8bb5ae0315d47c0a5de22a780229c7))
* **history:** rename `change_history` to `history` ([592de1d](https://github.com/acdh-oeaw/apis-core-rdf/commit/592de1d454a77f0530ac2933e4a76cfbcfa9578d)), closes [#802](https://github.com/acdh-oeaw/apis-core-rdf/issues/802)
* **history:** use signal instead of method for setting timestamp ([ca5bf94](https://github.com/acdh-oeaw/apis-core-rdf/commit/ca5bf940d0cf9959fde7b5dd3b00424b31bffa39)), closes [#814](https://github.com/acdh-oeaw/apis-core-rdf/issues/814)

## [0.17.3](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.17.2...v0.17.3) (2024-04-17)


### Bug Fixes

* **history:** make history timezone aware ([c157479](https://github.com/acdh-oeaw/apis-core-rdf/commit/c157479fd84d1cd8d336b527d03cc107582fdc54)), closes [#789](https://github.com/acdh-oeaw/apis-core-rdf/issues/789)

## [0.17.2](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.17.1...v0.17.2) (2024-04-16)


### Bug Fixes

* **history:** sort history data directly in model, not in templatetag ([ace42ef](https://github.com/acdh-oeaw/apis-core-rdf/commit/ace42ef04a3a9379ba26e56ceb22862b88e7dd6f)), closes [#784](https://github.com/acdh-oeaw/apis-core-rdf/issues/784)

## [0.17.1](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.17.0...v0.17.1) (2024-04-15)


### Bug Fixes

* **core:** add a model_meta templatetag filter ([8b334c7](https://github.com/acdh-oeaw/apis-core-rdf/commit/8b334c75440e9b7da84cb90ccb2f8472c909b378))
* **generic:** use dal widget only for models with autocomplete endpoint ([1de88f0](https://github.com/acdh-oeaw/apis-core-rdf/commit/1de88f05d74f95b93e476057f31cddfcb1cd05a2)), closes [#764](https://github.com/acdh-oeaw/apis-core-rdf/issues/764)
* **relations:** Property fields unicode normalization ([f1dd3db](https://github.com/acdh-oeaw/apis-core-rdf/commit/f1dd3db7f9310de1c457e96f3fae00578e83e663))
* **relations:** save with update_fields ([c4fe0e3](https://github.com/acdh-oeaw/apis-core-rdf/commit/c4fe0e3949cb1d062fa541b3b01c5f28848537f5))
* **utils:** use verbose_name for relation card title ([7df428b](https://github.com/acdh-oeaw/apis-core-rdf/commit/7df428b95d08a0c37cf34103828e2cd413f62b7a))

## [0.17.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.16.0...v0.17.0) (2024-04-08)


### Features

* **apis_entities:** add method for retrieving merge url of instance ([e4c0cd9](https://github.com/acdh-oeaw/apis-core-rdf/commit/e4c0cd9d03ed71949074e54ac7e63a383e2ea8cf))
* **apis_entities:** import improvements for E53_Place imports ([bffebc7](https://github.com/acdh-oeaw/apis-core-rdf/commit/bffebc700ffd7b59d64b506f0502aa88d1ad9653))
* **generic:** add methods for retrieving permssion names ([0a48a72](https://github.com/acdh-oeaw/apis-core-rdf/commit/0a48a72cf64b7d8aee41581c6bcb828788b6d737))
* **history:** add new history plugin ([1c8550d](https://github.com/acdh-oeaw/apis-core-rdf/commit/1c8550d42ec6bcdd0d7defe4c1303491a5c6f92c)), closes [#340](https://github.com/acdh-oeaw/apis-core-rdf/issues/340) [#242](https://github.com/acdh-oeaw/apis-core-rdf/issues/242)


### Bug Fixes

* **apis_entities:** replace custom permission name logic ([3ff23cb](https://github.com/acdh-oeaw/apis-core-rdf/commit/3ff23cba1322ddb217692e7d621d276a297b2658))
* **core:** fix css for select2 autocompletes ([805e336](https://github.com/acdh-oeaw/apis-core-rdf/commit/805e3360fb27cfdebf25ff79afa35c25fee267c4)), closes [#330](https://github.com/acdh-oeaw/apis-core-rdf/issues/330)
* **generic:** let the importer give more meaningfull error messages ([f036445](https://github.com/acdh-oeaw/apis-core-rdf/commit/f0364453f8a9ebe1d069cf6498db5d59770e7fb4))
* **generic:** move permission check to individual rows ([d3eb810](https://github.com/acdh-oeaw/apis-core-rdf/commit/d3eb810ad535bab3aad9bb6ba8f133765fe5a2f1))


### Documentation

* **history:** add basic doc for new history plugin ([f3ee6c8](https://github.com/acdh-oeaw/apis-core-rdf/commit/f3ee6c8bad8524a27525eb4c9d578d0bf47ae525))

## [0.16.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.15.2...v0.16.0) (2024-03-27)


### ⚠ BREAKING CHANGES

* **apis_metainfo:** drop RootObject.deprecated_name

### Features

* **apis_entities:** surround navigation elements with block ([6b2fb49](https://github.com/acdh-oeaw/apis-core-rdf/commit/6b2fb494131d1333f5ac04bf9ddef826aac7bdf8))
* **apis_relations:** add and use PropertySubjObjFilter ([246b7f3](https://github.com/acdh-oeaw/apis-core-rdf/commit/246b7f3fa0f530c605f892bd6866719b4a9e427a))
* **generic:** add ContentTypeInstanceSerializer ([3307074](https://github.com/acdh-oeaw/apis-core-rdf/commit/33070747df9aad9bb51424ec433a9f389aeeee9a))
* **generic:** implement custom schema generator ([09a1d6d](https://github.com/acdh-oeaw/apis-core-rdf/commit/09a1d6d932028781a57b866397f0d94e6be5cd15))
* **generic:** introduce GenericFilterBackend and use it ([dac1f6d](https://github.com/acdh-oeaw/apis-core-rdf/commit/dac1f6dc970d634e2f456ccbf46e4395949a9188))
* **generic:** ship a JSON based and a newline based list widget ([8704d21](https://github.com/acdh-oeaw/apis-core-rdf/commit/8704d2154a936b18f4db7d0b68452ca74295fb88)), closes [#733](https://github.com/acdh-oeaw/apis-core-rdf/issues/733)


### Bug Fixes

* **apis_metainfo:** drop RootObject.deprecated_name ([5fc11d7](https://github.com/acdh-oeaw/apis-core-rdf/commit/5fc11d7750171ead51c9242cd0480f27b039d72b))
* **apis_relations:** reuse GenericTable.Meta.sequence for tables ([b15e587](https://github.com/acdh-oeaw/apis-core-rdf/commit/b15e5875ae78e4dda28413856a67929a96a08bd3)), closes [#716](https://github.com/acdh-oeaw/apis-core-rdf/issues/716)
* **generic:** fix typo in Import View ([b28de6e](https://github.com/acdh-oeaw/apis-core-rdf/commit/b28de6e430b874f96abdfa2b84b6551537a15b58))
* **generic:** use fallback if ModelViewSet attributes don't exist ([11e097d](https://github.com/acdh-oeaw/apis-core-rdf/commit/11e097d64b949f8171f44d1f26238c2ba6aeaad0))

## [0.15.2](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.15.1...v0.15.2) (2024-03-19)


### Bug Fixes

* **apis_entities:** don't duplicate equal values when mergin charfield ([67f2aa5](https://github.com/acdh-oeaw/apis-core-rdf/commit/67f2aa5d5f6836bd5aa27fb0cace2f7784ea91a0))
* **apis_metainfo:** use ContentType instead of custom caching ([58e6c25](https://github.com/acdh-oeaw/apis-core-rdf/commit/58e6c25a134ae3ef760d0e724c721d0ecb975cd3))
* **core:** drop webpage remains from template ([6b3573e](https://github.com/acdh-oeaw/apis-core-rdf/commit/6b3573e4dff37a15dac33c54f9a9d3d3bd45e127)), closes [#410](https://github.com/acdh-oeaw/apis-core-rdf/issues/410)
* **core:** remove hardcoded imprint pointing to 404 ([e8441d9](https://github.com/acdh-oeaw/apis-core-rdf/commit/e8441d965ecb87f6f9925889c1f4b88d3d8e5e1c)), closes [#415](https://github.com/acdh-oeaw/apis-core-rdf/issues/415)
* **generic:** typo in `module_paths` argument ([3f3b71e](https://github.com/acdh-oeaw/apis-core-rdf/commit/3f3b71e125eafa47193f4285ea241830b80dfd63))
* **generic:** use `import_string` instead of custom method ([591b1ca](https://github.com/acdh-oeaw/apis-core-rdf/commit/591b1ca9ccb1bd1cd0288fe48de2cdbc75599b89)), closes [#697](https://github.com/acdh-oeaw/apis-core-rdf/issues/697)

## [0.15.1](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.15.0...v0.15.1) (2024-03-11)


### Bug Fixes

* **utils:** make rdfimport parent model check more loose ([84b97d3](https://github.com/acdh-oeaw/apis-core-rdf/commit/84b97d341757365deb4abf2cff846306d9a5249f))

## [0.15.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.14.2...v0.15.0) (2024-03-07)


### ⚠ BREAKING CHANGES

* **apis_metainfo:** The renaming of RootObject's "name" field to "deprecated_name" affects all inheriting model classes as well as class Property. You will need to create new fields in your model classes to replace it/to preserve its contents before it gets dropped.
* **core:** projects using the `confirm_delete.html` template will have to change that. There is a replacement in `generic/generic_confirm_delete.html`.
* **apis_metainfo,apis_entities:** drop __str___ overrides

### Features

* **apis_entities:** implement default abstract entity classes ([b1ebd0a](https://github.com/acdh-oeaw/apis-core-rdf/commit/b1ebd0a7b4c5c388c65aa36704521f646c8aed64)), closes [#403](https://github.com/acdh-oeaw/apis-core-rdf/issues/403)
* **apis_relations:** add obj and subj class filter to triple filters ([4b890c4](https://github.com/acdh-oeaw/apis-core-rdf/commit/4b890c47ad97ec0579db3892d2d7d562cf5a7d2a)), closes [#668](https://github.com/acdh-oeaw/apis-core-rdf/issues/668)
* **generic:** allow to override serializer based on renderer ([676251d](https://github.com/acdh-oeaw/apis-core-rdf/commit/676251de08c58266dabdc37038a43e2deab7114d))


### Bug Fixes

* **apis_entities:** move duplicate button after other action buttons ([1683968](https://github.com/acdh-oeaw/apis-core-rdf/commit/1683968b1a994c155a5f4e36ec96cf2ee517d1c2)), closes [#694](https://github.com/acdh-oeaw/apis-core-rdf/issues/694)
* **apis_entities:** use `modelname` instead of `verbose_name` ([ef10a69](https://github.com/acdh-oeaw/apis-core-rdf/commit/ef10a69ba8e66d86f42128789b7facdc9e39df73))
* **apis_entities:** use modelname instead of verbose_name in javascript ([6fee852](https://github.com/acdh-oeaw/apis-core-rdf/commit/6fee852c3ee1084b7d4ad345efaf2a6464f16370))
* **generic:** pass existing queryset to custom queryset ([12d4ed8](https://github.com/acdh-oeaw/apis-core-rdf/commit/12d4ed8c22eeb584df122d1c37cde7e1ee780d6a))


### Code Refactoring

* **apis_metainfo,apis_entities:** drop __str___ overrides ([c9fbcc8](https://github.com/acdh-oeaw/apis-core-rdf/commit/c9fbcc8f43320dbe1a0b188b14a0a8939fadbe81))
* **apis_metainfo:** rename RootObject.name to deprecated_name ([fcd4854](https://github.com/acdh-oeaw/apis-core-rdf/commit/fcd485453e88f5247f56c0f92f78ab3772852ece)), closes [#299](https://github.com/acdh-oeaw/apis-core-rdf/issues/299)
* **core:** drop unused template ([391f2de](https://github.com/acdh-oeaw/apis-core-rdf/commit/391f2dea9d0452e40efcc1f312497941c1ce99ff)), closes [#518](https://github.com/acdh-oeaw/apis-core-rdf/issues/518)

## [0.14.2](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.14.1...v0.14.2) (2024-02-29)


### Bug Fixes

* **apis_metainfo:** let Collection inherit from GenericModel ([0e32a80](https://github.com/acdh-oeaw/apis-core-rdf/commit/0e32a804c322b4b6448342d9f0f04b2cca0e04a5))

## [0.14.1](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.14.0...v0.14.1) (2024-02-29)


### Bug Fixes

* **generic,core:** move htmx setup from generic template to base.html ([bc4ba98](https://github.com/acdh-oeaw/apis-core-rdf/commit/bc4ba98033db560a02bff058938bdafebc8ecfb9))
* **generic:** use serializer_factory even with custom serializers ([247200e](https://github.com/acdh-oeaw/apis-core-rdf/commit/247200ebc075e557e450a92447ceb54ffa0fb72b))

## [0.14.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.13.1...v0.14.0) (2024-02-27)


### ⚠ BREAKING CHANGES

* **generic:** projects will have to inherit from `GenericModel` from now on, if they want their models to be accessible via the generic views. Models inheriting from APIS models automatically inherit from `GenericModel`.

### Features

* **generic:** use lru cache for smaller methods ([7e56e48](https://github.com/acdh-oeaw/apis-core-rdf/commit/7e56e480a141e81c5920df022e3d66e0c5c193ff))
* **utils:** provide some abstract base classes for autocomplete ([b3d2cbe](https://github.com/acdh-oeaw/apis-core-rdf/commit/b3d2cbecb34eb2e680139e9b57e502dbb561d558)), closes [#653](https://github.com/acdh-oeaw/apis-core-rdf/issues/653)


### Bug Fixes

* **apis_entities:** make import form deal with html data ([e7882e2](https://github.com/acdh-oeaw/apis-core-rdf/commit/e7882e253d950416d46f27af6c7b994e2362b838))
* **apis_entities:** remove buggy jQuery code ([f4fd17e](https://github.com/acdh-oeaw/apis-core-rdf/commit/f4fd17e21897eecc2f8801ffefef0267c0fe0fa6)), closes [#529](https://github.com/acdh-oeaw/apis-core-rdf/issues/529)
* **apis_relations:** remove choice limit in Property ([babfe4e](https://github.com/acdh-oeaw/apis-core-rdf/commit/babfe4ecabb3567b00e2970048e3ea653f20c0c4)), closes [#412](https://github.com/acdh-oeaw/apis-core-rdf/issues/412)
* **generic:** add `__init__.py` to generic module ([a74d445](https://github.com/acdh-oeaw/apis-core-rdf/commit/a74d4457de1567c1c0e911624ea508f195da95cb))
* **utils:** make rdf parser more robust ([d3ba5e3](https://github.com/acdh-oeaw/apis-core-rdf/commit/d3ba5e369b9eb2a88eb101b2adefadc7402ce85f)), closes [#666](https://github.com/acdh-oeaw/apis-core-rdf/issues/666)
* **utils:** refactor `access_for_all` ([b021696](https://github.com/acdh-oeaw/apis-core-rdf/commit/b0216968d67b21e1374968156e898a92e0cd831d)), closes [#582](https://github.com/acdh-oeaw/apis-core-rdf/issues/582)


### Documentation

* cleanup configuration section and rename it to `settings` ([d2c141c](https://github.com/acdh-oeaw/apis-core-rdf/commit/d2c141cb835df8cbdc1691e533b9a2ab61e30808))
* **generic:** add documentation about `GenericModel` ([54fbb09](https://github.com/acdh-oeaw/apis-core-rdf/commit/54fbb09e89d04b15b8eb38ec5af85263f7e4eb5b))


### Code Refactoring

* **generic:** introduce `generic.abc.GenericModel` ([8a58abc](https://github.com/acdh-oeaw/apis-core-rdf/commit/8a58abcc817267808c55a2d187d3dfe230599de8)), closes [#657](https://github.com/acdh-oeaw/apis-core-rdf/issues/657)

## [0.13.1](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.13.0...v0.13.1) (2024-02-15)


### Bug Fixes

* **apis_entities:** hide duplicate button on missing permission ([096181f](https://github.com/acdh-oeaw/apis-core-rdf/commit/096181fdaaca4fbb3caa4d06260e19abb2290acb))
* **apis_relations:** linkify subject and object columns ([bd1ed3d](https://github.com/acdh-oeaw/apis-core-rdf/commit/bd1ed3d45bdbcbba9979cbb586de0bdbb5dc8937)), closes [#1](https://github.com/acdh-oeaw/apis-core-rdf/issues/1)
* **generic:** check for permissions in actions nav ([0ec25df](https://github.com/acdh-oeaw/apis-core-rdf/commit/0ec25dfae9d7b7802521a1916a13e40506036fdd))
* **generic:** hide create button if permission does not exist ([154d2dd](https://github.com/acdh-oeaw/apis-core-rdf/commit/154d2dd3928f801fbb3a93671baf42118d31d3de))
* **generic:** the relevant permission name is `change` not `edit` ([fcdb491](https://github.com/acdh-oeaw/apis-core-rdf/commit/fcdb491b17814733a50f9b77d833ea59bb1891c9))
* **generic:** use custom permission solution in views ([edb783e](https://github.com/acdh-oeaw/apis-core-rdf/commit/edb783ec69eb790a936c2cdf4dd4b65c09ca8f89))

## [0.13.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.12.6...v0.13.0) (2024-02-14)


### ⚠ BREAKING CHANGES

* **apis_entities:** with the removal of `filters.py` and `tables.py` your configuration in `APIS_ENTITIES` won't have any effect anymore. Please replace them with custom tables and custom filtersets. Also the the locations and names and structure of the templates changed, so you will have to update those.

### Features

* add collection name as css class to collection templates ([44e1cf1](https://github.com/acdh-oeaw/apis-core-rdf/commit/44e1cf128aab9b214f245da7019e74a4f7ec2490)), closes [#604](https://github.com/acdh-oeaw/apis-core-rdf/issues/604)
* **generic:** add debug log message to first_match_via_mro ([458ffd2](https://github.com/acdh-oeaw/apis-core-rdf/commit/458ffd2178532f6eac11c443374515be26e74c56))
* **generic:** display foreign key fields as value instead of id ([7936d8a](https://github.com/acdh-oeaw/apis-core-rdf/commit/7936d8aaaacb66dfee6a2a7f4534bdd525196cb3))
* **generic:** fix and enhance the generate_search_filter helper ([03eb3fe](https://github.com/acdh-oeaw/apis-core-rdf/commit/03eb3fe9c08f04ba676ff06de35aed496e12cf2a))
* **generic:** make GenericImporter more verbose ([63aa960](https://github.com/acdh-oeaw/apis-core-rdf/commit/63aa9600e8a42486d4a3fc41420ef6524f8d9261))
* **generic:** use `data-html` in autocomplete widgets ([c6d326f](https://github.com/acdh-oeaw/apis-core-rdf/commit/c6d326f676e039550abb8f4fda420cb9843c5aeb))
* **generic:** use template attribute of autocomplete view ([a9f0d38](https://github.com/acdh-oeaw/apis-core-rdf/commit/a9f0d38dc5a9850421ddfee60a335a8100aa84d3))
* **utils:** use dict_from_toml_directory for cleaning uris ([a703f51](https://github.com/acdh-oeaw/apis-core-rdf/commit/a703f513931e5cf957c8499f1ba1dfa05d79f728))


### Bug Fixes

* **apis_entities:** f string in merge_textfield missing f ([2b7bdb9](https://github.com/acdh-oeaw/apis-core-rdf/commit/2b7bdb951410deae0dee4443d77cdacf06d5be65))
* **apis_entities:** fix wikidata uri mapping ([7372ff1](https://github.com/acdh-oeaw/apis-core-rdf/commit/7372ff16f7e7688561ca81aaef4ba68d0cf613e5))
* **apis_metainfo:** set the `alters_data` attribute of duplicate ([d5cfdb5](https://github.com/acdh-oeaw/apis-core-rdf/commit/d5cfdb55cb005d3967bfd04aad7130526225d93b))
* **apis_relations:** don't rely on APIS_BASE_URI for editing relations ([39f2cf1](https://github.com/acdh-oeaw/apis-core-rdf/commit/39f2cf189cb0705bc03efd40664db8da7754ec8b))
* **apis_relations:** use generic autocomplete in GenericTripleForm ([0b23cc7](https://github.com/acdh-oeaw/apis-core-rdf/commit/0b23cc7c7535e945ee36b2213aa5350f495476d6))
* **generic:** don't set template_name_suffix, only use it if its set ([71aef12](https://github.com/acdh-oeaw/apis-core-rdf/commit/71aef12645aa8b4a5b655a1e0cac40e54255ba54))
* **generic:** redirect to update view after create or update ([1faf5c4](https://github.com/acdh-oeaw/apis-core-rdf/commit/1faf5c472cd5f65e648bef99c89a3964d10b452d))


### Documentation

* **generic:** add documentation about generic app customization ([6de3708](https://github.com/acdh-oeaw/apis-core-rdf/commit/6de370891d0b450afc44eefd1062a899dcfcdfec))


### Code Refactoring

* **apis_entities:** use new generic app ([45de48b](https://github.com/acdh-oeaw/apis-core-rdf/commit/45de48bea2b81823873066820a079635b8d7a04a))

## [0.12.6](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.12.5...v0.12.6) (2024-01-31)


### Bug Fixes

* let the autocomplete form create objects ([a07f23b](https://github.com/acdh-oeaw/apis-core-rdf/commit/a07f23beed83614832c085b6de0f9a46008eb34f))

## [0.12.5](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.12.4...v0.12.5) (2024-01-31)


### Bug Fixes

* exclude `metadata` field from legacy api viewset stuff ([dd2fb57](https://github.com/acdh-oeaw/apis-core-rdf/commit/dd2fb578b99e7a8cebd388576c6ad10971a889be))

## [0.12.4](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.12.3...v0.12.4) (2024-01-31)


### Bug Fixes

* **generic:** don't allow access to `admin`, `auth` and `sessions` ([ff43fc8](https://github.com/acdh-oeaw/apis-core-rdf/commit/ff43fc846ca94718b1d23533a1d836e92c8c0ef5))

## [0.12.3](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.12.2...v0.12.3) (2024-01-31)


### Bug Fixes

* **apis_entities:** add more information to autocomplete results ([db1c0c7](https://github.com/acdh-oeaw/apis-core-rdf/commit/db1c0c73b038e93e75feb0a71e691f1bb2c0ea13))
* **generic:** only show table actions if user has required permissions ([79d74a3](https://github.com/acdh-oeaw/apis-core-rdf/commit/79d74a317aa3e2b8a50595b81456f72f21a4ae5e)), closes [#584](https://github.com/acdh-oeaw/apis-core-rdf/issues/584)

## [0.12.2](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.12.1...v0.12.2) (2024-01-30)


### Bug Fixes

* use the ListViewObjectFilterMixin in the generic.views.List view ([94734dc](https://github.com/acdh-oeaw/apis-core-rdf/commit/94734dc425333edf04b1f0f9268dcf9941ce79f1))

## [0.12.1](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.12.0...v0.12.1) (2024-01-30)


### Bug Fixes

* **api_routers:** fix generic_serializer_creation_factory ([eeb7430](https://github.com/acdh-oeaw/apis-core-rdf/commit/eeb743086cb9cca725e7f9401d2e028302db467b)), closes [#577](https://github.com/acdh-oeaw/apis-core-rdf/issues/577)
* drop TextSerializer and use GenericHyperlinkedModelSerializer ([5c0091b](https://github.com/acdh-oeaw/apis-core-rdf/commit/5c0091baee43515ca9bc2fff5e18f52f789e2c97))

## [0.12.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.11.3...v0.12.0) (2024-01-30)


### Features

* **generic:** allow to extend autocomplete results with custom results ([cbad572](https://github.com/acdh-oeaw/apis-core-rdf/commit/cbad572207d419e5a8ed5be1d8bb8315054cd407))
* **generic:** implement extendable importer ([06ad57b](https://github.com/acdh-oeaw/apis-core-rdf/commit/06ad57b629c912f9419024e77bc4aff299a518fe)), closes [#541](https://github.com/acdh-oeaw/apis-core-rdf/issues/541)


### Documentation

* document extending the autocomplete endpoint ([8f1613b](https://github.com/acdh-oeaw/apis-core-rdf/commit/8f1613b7b52cede4d58962e4b6fbf2c434f4be16))
* document importing data from external resources ([280413e](https://github.com/acdh-oeaw/apis-core-rdf/commit/280413e4fe607d6a5500484a527840c0bf736058))
* update readme ([bba2c8c](https://github.com/acdh-oeaw/apis-core-rdf/commit/bba2c8c0b8acbe16f45f8414d5970de4cc6c3bee))

## [0.11.3](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.11.2...v0.11.3) (2024-01-26)


### Bug Fixes

* **apis_entities:** fix accidently removed form save ([33792cc](https://github.com/acdh-oeaw/apis-core-rdf/commit/33792cc277360d73abc4b88cd2be6a9addc8ca7e))

## [0.11.2](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.11.1...v0.11.2) (2024-01-26)


### Bug Fixes

* add missing skoscollection migration ([7c8d861](https://github.com/acdh-oeaw/apis-core-rdf/commit/7c8d861341747efa49cb795f03b75cf181ea1d22))
* **generic:** the permission string must also contain the app_label ([8140a3d](https://github.com/acdh-oeaw/apis-core-rdf/commit/8140a3db3e6b95550947a1254cde2ad1ec9d2fc8))

## [0.11.1](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.11.0...v0.11.1) (2024-01-25)


### Bug Fixes

* **collections:** add collection_content_objects templatetag ([865754a](https://github.com/acdh-oeaw/apis-core-rdf/commit/865754abe1926d7fde4e6db6edb4fb24790d8c52))
* **collections:** set default order of SkosCollection ([88543d2](https://github.com/acdh-oeaw/apis-core-rdf/commit/88543d2db2b15ea4fc4095402b4cd9f956fd5110))
* let users override generic views ([7b30880](https://github.com/acdh-oeaw/apis-core-rdf/commit/7b308808969503a5ea97b304e8f310247e9c45d3))

## [0.11.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.10.1...v0.11.0) (2024-01-24)


### Features

* add collections app ([6e6753e](https://github.com/acdh-oeaw/apis-core-rdf/commit/6e6753e15a4aa905634805e40d58f97191c60f92))
* allow to exclude fields from table columns ([92cba82](https://github.com/acdh-oeaw/apis-core-rdf/commit/92cba8214e02e4b0cfc081016821e234f389a5da))


### Documentation

* add documentation for new collections app ([e5020be](https://github.com/acdh-oeaw/apis-core-rdf/commit/e5020be1eab755b99b80285b9885ae5b155f817f))

## [0.10.1](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.10.0...v0.10.1) (2024-01-19)


### Bug Fixes

* **generic:** backport `filterset_factory` from django-filters ([c235107](https://github.com/acdh-oeaw/apis-core-rdf/commit/c235107154ab50a1e90b9a5f1aba8d324fdc0df9))
* **generic:** filter the iterator before returning the first element ([a6fba0f](https://github.com/acdh-oeaw/apis-core-rdf/commit/a6fba0f0d362158d768926196733567d392f983c))

## [0.10.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.9.1...v0.10.0) (2024-01-18)


### ⚠ BREAKING CHANGES

* **apis_entities:** drop TempEntityClass
* **apis_vocabularies:** remove apis_vocabularies app

### Features

* add htmx to base template ([f33b707](https://github.com/acdh-oeaw/apis-core-rdf/commit/f33b7075dfed00c765d264edcac25ebbfc247f57))
* introduce generic app ([edb7a88](https://github.com/acdh-oeaw/apis-core-rdf/commit/edb7a884f6afe3542d27c6c749f8091a47d8ad64)), closes [#509](https://github.com/acdh-oeaw/apis-core-rdf/issues/509)


### Bug Fixes

* **apis_entities:** drop TempEntityClass ([b08bfb6](https://github.com/acdh-oeaw/apis-core-rdf/commit/b08bfb6f27df35f5f7c8c185ab4e8cb0a9e69791)), closes [#6](https://github.com/acdh-oeaw/apis-core-rdf/issues/6)
* drop collectiontype field from Collection model ([c74f628](https://github.com/acdh-oeaw/apis-core-rdf/commit/c74f6280991fc388c27dc1eadf2f5e7f000be345))


### Code Refactoring

* **apis_vocabularies:** remove apis_vocabularies app ([e89e03d](https://github.com/acdh-oeaw/apis-core-rdf/commit/e89e03dc2e9ce3562bac5c9a7a3b6bf619a23135)), closes [#514](https://github.com/acdh-oeaw/apis-core-rdf/issues/514)

## [0.9.1](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.9.0...v0.9.1) (2023-12-21)


### Bug Fixes

* deletion of entity objects ([e95e030](https://github.com/acdh-oeaw/apis-core-rdf/commit/e95e030bcb40553e96df6334f121bb5927247bb8)), closes [#485](https://github.com/acdh-oeaw/apis-core-rdf/issues/485)

## [0.9.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.8.1...v0.9.0) (2023-12-19)


### ⚠ BREAKING CHANGES

* drop EntityToProsopogrAPhI API endpoint
* drop `resolve_abbrevations` command
* drop `apis_vocabularies.models.TextType`
* drop `apis_vocabularies.models.LabelType`
* **deps:** django-crispy-forms uses separate template packs since version 2. we depend on crispy-bootstrap4 by default, but projects have to add `crispy_bootstrap4` to the INSTALLED_APPS themselves.
* **apis_labels:** APIS projects will have to remove `apis_core.apis_labels` from their settings `INSTALLED_APPS`

### Features

* **apis_labels:** drop apis_labels ([0c44287](https://github.com/acdh-oeaw/apis-core-rdf/commit/0c44287eac678f40a24c98ffe8b7efb053487db4)), closes [#15](https://github.com/acdh-oeaw/apis-core-rdf/issues/15)
* improve listview pagination ([13088b6](https://github.com/acdh-oeaw/apis-core-rdf/commit/13088b62ffe62ac12599bf91d80c114f3a735f78)), closes [#416](https://github.com/acdh-oeaw/apis-core-rdf/issues/416)


### Bug Fixes

* allow `dumpdata` API access for all authenticated users ([a2ffbfd](https://github.com/acdh-oeaw/apis-core-rdf/commit/a2ffbfd1f7fa96018c79894b3e072f66df8301e2))


### Miscellaneous Chores

* **deps:** add crispy-bootstrap4 as dependency ([759e0c6](https://github.com/acdh-oeaw/apis-core-rdf/commit/759e0c60143b854b706c226293a3c64fd19bab65))


### Code Refactoring

* drop `apis_vocabularies.models.LabelType` ([d690d93](https://github.com/acdh-oeaw/apis-core-rdf/commit/d690d9313805f1f1d582b1689bea2dfa1d9b64c1)), closes [#498](https://github.com/acdh-oeaw/apis-core-rdf/issues/498)
* drop `apis_vocabularies.models.TextType` ([22562cb](https://github.com/acdh-oeaw/apis-core-rdf/commit/22562cbefa82a9aeca94c32e2b2c4b9cfa33fe84)), closes [#499](https://github.com/acdh-oeaw/apis-core-rdf/issues/499)
* drop `resolve_abbrevations` command ([7c3edd8](https://github.com/acdh-oeaw/apis-core-rdf/commit/7c3edd810be7fa6f12c40766dc292d0985fb81ea)), closes [#501](https://github.com/acdh-oeaw/apis-core-rdf/issues/501)
* drop EntityToProsopogrAPhI API endpoint ([0448fec](https://github.com/acdh-oeaw/apis-core-rdf/commit/0448fec6fa715a195dadfc60ec415f4ca64099c3))

## [0.8.1](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.8.0...v0.8.1) (2023-12-14)


### Bug Fixes

* checks if collections exist in merge function ([f9c5d6d](https://github.com/acdh-oeaw/apis-core-rdf/commit/f9c5d6d14fdc9329a58dfc147db732e05f3bb7ee)), closes [#492](https://github.com/acdh-oeaw/apis-core-rdf/issues/492)

## [0.8.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.7.1...v0.8.0) (2023-12-13)


### ⚠ BREAKING CHANGES

* APIS projects will have to remove the `custom_context_processors` from the list of used `context_processors`
* **apis_entites:** any template in your ontology that inherits from the person_detail_generic template needs to point to the detail_generic template instead

### Features

* **apis_entites:** remove person detail template ([75753d4](https://github.com/acdh-oeaw/apis-core-rdf/commit/75753d49dae4dd2850754fcc3afb44dcd110f80b)), closes [#397](https://github.com/acdh-oeaw/apis-core-rdf/issues/397)
* implement dumpdata view and admin command ([9115fc9](https://github.com/acdh-oeaw/apis-core-rdf/commit/9115fc96bd616e3a0f0d2a5d1fc9b18330fee836)), closes [#273](https://github.com/acdh-oeaw/apis-core-rdf/issues/273)
* let projects override entities forms using classes ([14a2489](https://github.com/acdh-oeaw/apis-core-rdf/commit/14a24898a19fd41e441533d280f02ed16858ac9a))


### Bug Fixes

* drop meta_fields from forms ([378d162](https://github.com/acdh-oeaw/apis-core-rdf/commit/378d1622ac10e938c02f0c411ca06a353b14ff61)), closes [#475](https://github.com/acdh-oeaw/apis-core-rdf/issues/475)
* drop unused code block ([a8488f3](https://github.com/acdh-oeaw/apis-core-rdf/commit/a8488f383458eee8ec02fa60e347195365e8509f))
* drop unused custom context processors ([5b2bfd6](https://github.com/acdh-oeaw/apis-core-rdf/commit/5b2bfd6de18e074edcc52282943e054d06e19f39))
* link to delete view in entity edit template ([5503a6d](https://github.com/acdh-oeaw/apis-core-rdf/commit/5503a6dbbf89baf3fd6fa3fd7a379136cc3b960e)), closes [#437](https://github.com/acdh-oeaw/apis-core-rdf/issues/437)
* provide a fallback template if basetemplate is not set ([2ee69ce](https://github.com/acdh-oeaw/apis-core-rdf/commit/2ee69ce6b3402b5e598805d0f52155ddfcd919f3))


### Documentation

* drop PyYAML from dependency list, add apis-override-select2js ([087ed95](https://github.com/acdh-oeaw/apis-core-rdf/commit/087ed957070a37cea4157aaf964f2e44c2294c8e))


### Code Refactoring

* drop custom_context_processors ([c3d7155](https://github.com/acdh-oeaw/apis-core-rdf/commit/c3d7155c0756a8f58470e20a3474c7acc2ecddac))

## [0.7.1](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.7.0...v0.7.1) (2023-11-27)


### Bug Fixes

* cleanup generic edit template ([18234e7](https://github.com/acdh-oeaw/apis-core-rdf/commit/18234e710235eacb83b095bc7eb48c70e09de020))
* integrate django.contrib.auth.urls into apis_core.urls ([39a63f4](https://github.com/acdh-oeaw/apis-core-rdf/commit/39a63f40f3000bb68d76f6e550d9657bc77c2ec6)), closes [#426](https://github.com/acdh-oeaw/apis-core-rdf/issues/426)
* override default for JSONField field ([18c05dd](https://github.com/acdh-oeaw/apis-core-rdf/commit/18c05ddcdc93318e6898ca295b30095d1cd6b306))
* rewrite error message ([d560fe8](https://github.com/acdh-oeaw/apis-core-rdf/commit/d560fe815f4322d5265b4ee60cb3fab68854da05))


### Documentation

* add CONTRIBUTING.md ([fe8f46b](https://github.com/acdh-oeaw/apis-core-rdf/commit/fe8f46bb72a1838234df1becffab4bc4208f680d)), closes [#425](https://github.com/acdh-oeaw/apis-core-rdf/issues/425)

## [0.7.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.6.3...v0.7.0) (2023-11-14)


### ⚠ BREAKING CHANGES

* get rid of additional_serializer

### Features

* allow overriding the entity listview queryset ([0548faa](https://github.com/acdh-oeaw/apis-core-rdf/commit/0548faab7ac1a99266e5b728de00d373d688b76a))
* introduce `get_member_for_entity` helper ([6436f2f](https://github.com/acdh-oeaw/apis-core-rdf/commit/6436f2f15219daf1c423f4426c6531c40720bd7e))


### Bug Fixes

* cleanup entities detail template ([87834b3](https://github.com/acdh-oeaw/apis-core-rdf/commit/87834b3bfde1edbd75648533103ae5ff0d09f6df)), closes [#396](https://github.com/acdh-oeaw/apis-core-rdf/issues/396)
* don't expect entities to have {start|end}_date_written fields ([4952af2](https://github.com/acdh-oeaw/apis-core-rdf/commit/4952af24727fff9115e84cd9200c9da9af9eaffb)), closes [#405](https://github.com/acdh-oeaw/apis-core-rdf/issues/405)
* drop object_revisions from generic entities edit view ([f08b10c](https://github.com/acdh-oeaw/apis-core-rdf/commit/f08b10c99fccb30a48134e02651c60125aba3fa0))
* improve `get_member_for_entity` helper function ([1f9a1a0](https://github.com/acdh-oeaw/apis-core-rdf/commit/1f9a1a00b368f95000d331ad37fdb9efa6be604c))
* use the new `get_member_for_entity` helper to override table ([caa6f65](https://github.com/acdh-oeaw/apis-core-rdf/commit/caa6f65fa6b1db7a9cd5030d43d32f4b050396ed)), closes [#400](https://github.com/acdh-oeaw/apis-core-rdf/issues/400)


### Documentation

* make install instructions more clear ([e6a4efe](https://github.com/acdh-oeaw/apis-core-rdf/commit/e6a4efe9d243e9eab151ebbd3c85829d4defeb56))


### Code Refactoring

* get rid of additional_serializer ([190e5f3](https://github.com/acdh-oeaw/apis-core-rdf/commit/190e5f3f95b1fd2d7351e6807e27e3acdafd7d80)), closes [#338](https://github.com/acdh-oeaw/apis-core-rdf/issues/338)

## [0.6.3](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.6.2...v0.6.3) (2023-11-08)


### Bug Fixes

* add apis-override-select2js to dependencies ([697b4e1](https://github.com/acdh-oeaw/apis-core-rdf/commit/697b4e14ebb6313e1b6435984e3b07975817c47e)), closes [#389](https://github.com/acdh-oeaw/apis-core-rdf/issues/389)
* do not expect fields in EntitySerializer ([e4480f3](https://github.com/acdh-oeaw/apis-core-rdf/commit/e4480f3ac1d56a5ff3fa4757cc00e2664d6854a9)), closes [#383](https://github.com/acdh-oeaw/apis-core-rdf/issues/383)
* use RootObject instead of TempEntityClass in GetEntityGeneric ([d03fad5](https://github.com/acdh-oeaw/apis-core-rdf/commit/d03fad57265c4463bbafbf299f2ac2c95b7096a0)), closes [#380](https://github.com/acdh-oeaw/apis-core-rdf/issues/380)


### Documentation

* rearrange installation info and add URL dispatcher info ([7d9fff3](https://github.com/acdh-oeaw/apis-core-rdf/commit/7d9fff3008ec164fb71f43413726f2a07932401e)), closes [#393](https://github.com/acdh-oeaw/apis-core-rdf/issues/393)
* update README, now that apis-override-select2js is a dependency ([f23e9eb](https://github.com/acdh-oeaw/apis-core-rdf/commit/f23e9eb937a6bf74565af2cadce4f1a0591a5c67))

## [0.6.2](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.6.1...v0.6.2) (2023-10-20)


### Bug Fixes

* add `setuptools` as django-model-utils dependency ([de3a10a](https://github.com/acdh-oeaw/apis-core-rdf/commit/de3a10a71f6a9f25085cbb137b9e1553753aacb4))
* drop `get_child_class()` from AbstractEntity ([e10c661](https://github.com/acdh-oeaw/apis-core-rdf/commit/e10c661ed0bff8e996d9ad2e850aafb909923de3)), closes [#323](https://github.com/acdh-oeaw/apis-core-rdf/issues/323)
* move management command ([f3097ba](https://github.com/acdh-oeaw/apis-core-rdf/commit/f3097baddadf76edf6045a7ceb04a4fe452f688b)), closes [#372](https://github.com/acdh-oeaw/apis-core-rdf/issues/372)
* surround embedding of custom stylesheet with if statement ([039f9d4](https://github.com/acdh-oeaw/apis-core-rdf/commit/039f9d46058b59238b747be9ac16dfa9ca6920b9)), closes [#364](https://github.com/acdh-oeaw/apis-core-rdf/issues/364)
* **ux:** add nav class in template block ([d389856](https://github.com/acdh-oeaw/apis-core-rdf/commit/d3898567810bae976a0286e0b2cd3bd33cce0754))


### Documentation

* drop the poetry add line, as those are all dependencies ([5c61809](https://github.com/acdh-oeaw/apis-core-rdf/commit/5c618098fdd2cc6713aa82826ec6ec0584fc776b))
* start documenting development practices ([025186f](https://github.com/acdh-oeaw/apis-core-rdf/commit/025186f37fcbc6244022e1ed911547da4cd01903))
* update README.md ([8c74d97](https://github.com/acdh-oeaw/apis-core-rdf/commit/8c74d97b6de82022aa157ad5351bbac68ec89921)), closes [#361](https://github.com/acdh-oeaw/apis-core-rdf/issues/361)

## [0.6.1](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.6.0...v0.6.1) (2023-10-18)


### Bug Fixes

* drop `collections` as default field from entities filter ([05e8ad9](https://github.com/acdh-oeaw/apis-core-rdf/commit/05e8ad9dffd36c6244105fe8a909da9f5dd6be9e)), closes [#354](https://github.com/acdh-oeaw/apis-core-rdf/issues/354)
* instead of pointing to admin, use the user login/logout routes ([a5073db](https://github.com/acdh-oeaw/apis-core-rdf/commit/a5073dbdf7bcecb7f185f9a212f421f4e3dcd316)), closes [#353](https://github.com/acdh-oeaw/apis-core-rdf/issues/353)
* put footer and imprint in separate template blocks ([53b3e10](https://github.com/acdh-oeaw/apis-core-rdf/commit/53b3e10a4f589a73d7163a58ee8bfeab59e879f2)), closes [#345](https://github.com/acdh-oeaw/apis-core-rdf/issues/345)
* readd exclude list of fields in detail view and allow customization ([0bd2446](https://github.com/acdh-oeaw/apis-core-rdf/commit/0bd2446cc590a04c144b819da87f2dcdca69e940))
* use value from model_to_dict instead of getattr ([2e2f5fe](https://github.com/acdh-oeaw/apis-core-rdf/commit/2e2f5fedf5b4494b010fbbf8d58b73702f85869a))

## [0.6.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.5.0...v0.6.0) (2023-10-16)


### ⚠ BREAKING CHANGES

* drop the charts dependency
* if the GenericEntityListFilter was used with the `method` set to one of the included methods, the `method` attribute should now point to `apis_core.utils.filtermethods...`

### Features

* add Property to admin interface ([b11352d](https://github.com/acdh-oeaw/apis-core-rdf/commit/b11352dbfa29ce9f062b626c224a4f62829ffd4f))


### Bug Fixes

* add slash to `shared_url` templatetag ([ff47d2a](https://github.com/acdh-oeaw/apis-core-rdf/commit/ff47d2aadf75cfe6936e5cc3a9f37ad9101f1cb1))
* fixes `merge_with` function expecting TempEntityClass ([e40ecb3](https://github.com/acdh-oeaw/apis-core-rdf/commit/e40ecb32d11ecbc6024173d5f40341a66b6741f2))
* introduce APIS_LIST_LINKS_TO_EDIT variable ([8bc259c](https://github.com/acdh-oeaw/apis-core-rdf/commit/8bc259ca24f03da35ae659a84d38314dc5801a33))
* migrate management commands from `apis-webpage` to `apis-rdf-core` ([09fac5e](https://github.com/acdh-oeaw/apis-core-rdf/commit/09fac5ee9f1bc20d21610326bfa3b74e42b63cf5))
* put function call in separate document.ready function ([dd51f5b](https://github.com/acdh-oeaw/apis-core-rdf/commit/dd51f5b394de077c84eab22913d2db83534459af))
* remove duplicate of `references` attribute in detail view ([a381b02](https://github.com/acdh-oeaw/apis-core-rdf/commit/a381b028cb25637dd638f11c03181a8a9c5dc238))
* the contenttype of the rootobject should not be user editable ([872386e](https://github.com/acdh-oeaw/apis-core-rdf/commit/872386eb35640f1bf13b8716e5ac696422ffc970))


### Documentation

* reference `utils.filtermethods` in configuration ([8b6700d](https://github.com/acdh-oeaw/apis-core-rdf/commit/8b6700d497e42ce3682d063d7f8226c25f441652))


### Code Refactoring

* drop the charts dependency ([c963cd8](https://github.com/acdh-oeaw/apis-core-rdf/commit/c963cd83b7d4e5c32471da6f1d7cb73dbcfe19ff))
* move filtermethods from apis_entities to utils ([5068b49](https://github.com/acdh-oeaw/apis-core-rdf/commit/5068b49633693be0d5054672fe9252b5ee5e0037)), closes [#152](https://github.com/acdh-oeaw/apis-core-rdf/issues/152)

## [0.5.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.4.0...v0.5.0) (2023-10-05)


### ⚠ BREAKING CHANGES

* **apis_metainfo:** drop `Source` model
* drop apis module

### Features

* cleanup the default entity detail and edit view ([8011894](https://github.com/acdh-oeaw/apis-core-rdf/commit/80118942af1b6c3603561f3f0e10cd0837fb6df5))
* introduce new templatetags ([0ce7df4](https://github.com/acdh-oeaw/apis-core-rdf/commit/0ce7df4e34efc31b5b3c80374b70889ffbe7938e)), closes [#293](https://github.com/acdh-oeaw/apis-core-rdf/issues/293)
* put main-menu submenu items in separate blocks ([45e031e](https://github.com/acdh-oeaw/apis-core-rdf/commit/45e031e72efa34362c5bff01830c8f2bb6aed6b4)), closes [#306](https://github.com/acdh-oeaw/apis-core-rdf/issues/306)


### Bug Fixes

* allow overriding the entity form ([f56ef89](https://github.com/acdh-oeaw/apis-core-rdf/commit/f56ef89a571c1eafdbd5b7d09034735f8d30af2e)), closes [#238](https://github.com/acdh-oeaw/apis-core-rdf/issues/238)
* **apis_entities:** only set collection if the attribute exists ([e7be0ec](https://github.com/acdh-oeaw/apis-core-rdf/commit/e7be0ecd3727ecc8db461e1e1636412bfef2ba48)), closes [#313](https://github.com/acdh-oeaw/apis-core-rdf/issues/313)
* build docs without apis module ([b44a706](https://github.com/acdh-oeaw/apis-core-rdf/commit/b44a706e16129b19a463e308619c14a59a42bf7b))
* get rid of text model remains ([8a90be2](https://github.com/acdh-oeaw/apis-core-rdf/commit/8a90be2bf2a6ffcd5ffd6c7af8530cfac9618eb0))
* workaround for entities not inheriting from TempEntityClass ([9ba5778](https://github.com/acdh-oeaw/apis-core-rdf/commit/9ba5778dd3762d9da834cdad277e9f268ac4f17a))


### Code Refactoring

* **apis_metainfo:** drop `Source` model ([e877213](https://github.com/acdh-oeaw/apis-core-rdf/commit/e877213bb431666f9a0cf826433d5196abbfaeb7)), closes [#227](https://github.com/acdh-oeaw/apis-core-rdf/issues/227)
* drop apis module ([cd16eb1](https://github.com/acdh-oeaw/apis-core-rdf/commit/cd16eb19006f1f6a0d2477e32da424026b0a8edb)), closes [#222](https://github.com/acdh-oeaw/apis-core-rdf/issues/222)

## [0.4.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.3.1...v0.4.0) (2023-09-27)


### Features

* replaces feather icons with material-symbols ([1d85d57](https://github.com/acdh-oeaw/apis-core-rdf/commit/1d85d57898594e8bd18b8f30be641a7cd0f97d72))


### Bug Fixes

* **api_routers:** allow to let the `id` field be writable in API ([71f85e6](https://github.com/acdh-oeaw/apis-core-rdf/commit/71f85e66ae077cdd2f527a73e40195c230ea9a4f)), closes [#296](https://github.com/acdh-oeaw/apis-core-rdf/issues/296)
* **apis_entities:** fix reversion for tempentity classes ([cfb1771](https://github.com/acdh-oeaw/apis-core-rdf/commit/cfb17712fc03d36ff2f77d402797d0957da046d3))
* **apis_entities:** only set field attributes for existing fields ([100de8c](https://github.com/acdh-oeaw/apis-core-rdf/commit/100de8c2b62fec99d021e14da8cf58764a4d594c)), closes [#298](https://github.com/acdh-oeaw/apis-core-rdf/issues/298)
* **apis_metainfo:** register the rootobject with reversion ([b7217b9](https://github.com/acdh-oeaw/apis-core-rdf/commit/b7217b9888516b7daa4a69d0191004c627a72207))
* **apis_relations:** fix entity lookup for multi URI entities ([0febd2a](https://github.com/acdh-oeaw/apis-core-rdf/commit/0febd2ab97e8ae0d673d3a13b890d46ee40c01a4)), closes [#221](https://github.com/acdh-oeaw/apis-core-rdf/issues/221)
* **apis_relations:** fix follow of property reveversion registration ([6e4df12](https://github.com/acdh-oeaw/apis-core-rdf/commit/6e4df122688fe4446ced9a52254c68fbfabdbfed))
* LegacyDateMixin get dates from DateParser datetimes ([78215e4](https://github.com/acdh-oeaw/apis-core-rdf/commit/78215e4ba0e69b1ad4b8b9dce7c5899ac18e6a70)), closes [#295](https://github.com/acdh-oeaw/apis-core-rdf/issues/295)
* use empty dict as fallback for PROJECT_DEFAULT_MD ([8aa5394](https://github.com/acdh-oeaw/apis-core-rdf/commit/8aa53943a3202194f15302bf42b14aae27d9d053))

## [0.3.1](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.3.0...v0.3.1) (2023-09-13)


### Bug Fixes

* add migrations forgotten in 063412f ([7fd93f3](https://github.com/acdh-oeaw/apis-core-rdf/commit/7fd93f353df7c7852e02a8c6ee1ca697185de37a))

## [0.3.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.2.0...v0.3.0) (2023-09-13)


### ⚠ BREAKING CHANGES

* **apis_entities, apis_metainfo:** drop texts
* **apis_metainfo:** cleanup menu block in base template

### Features

* **apis_entities:** enclose the relations listing in a relations block ([f052035](https://github.com/acdh-oeaw/apis-core-rdf/commit/f052035c8b582cc5b9536b635cd8dc965c2b589d))
* **apis_metainfo:** cleanup menu block in base template ([8f5943b](https://github.com/acdh-oeaw/apis-core-rdf/commit/8f5943b45248f10afcddc601cf2ec0f93a350344))
* **core:** add userlogin-menu block to `base.html` ([7bc4a29](https://github.com/acdh-oeaw/apis-core-rdf/commit/7bc4a29b8f3953f30a9e3f678f6e938e4e39023e))
* provide modal block in base template ([86f5d43](https://github.com/acdh-oeaw/apis-core-rdf/commit/86f5d4357908de6af240e523c1cf09db09421e99))


### Bug Fixes

* **apis_entities, apis_metainfo:** drop texts ([063412f](https://github.com/acdh-oeaw/apis-core-rdf/commit/063412fb28bb812325010bae333f19ea3cb7bd8d))
* **apis_metainfo:** drop `browsing/generic_list.html` template ([b5a9f7a](https://github.com/acdh-oeaw/apis-core-rdf/commit/b5a9f7ab8f433e1c957e52c58e4d31f5e3722c03)), closes [#151](https://github.com/acdh-oeaw/apis-core-rdf/issues/151)
* **deps:** loosen Python dependency ([0d37dcc](https://github.com/acdh-oeaw/apis-core-rdf/commit/0d37dcca921ca3ba8e6ce9b21ba2db4be7897e30)), closes [#255](https://github.com/acdh-oeaw/apis-core-rdf/issues/255)

## [0.2.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.1.1...v0.2.0) (2023-09-07)


### ⚠ BREAKING CHANGES

* **apis_metainfo:** rename templatetags
* **apis_vis:** drop apis_vis
* **apis_metainfo:** drop UriCandidate

### Features

* **apis_vis:** drop apis_vis ([7e69eb1](https://github.com/acdh-oeaw/apis-core-rdf/commit/7e69eb16cf324fcd8530d0f326a47d1ffc15202c)), closes [#206](https://github.com/acdh-oeaw/apis-core-rdf/issues/206)
* **core:** Introduce LegacyDateMixin ([fe3c205](https://github.com/acdh-oeaw/apis-core-rdf/commit/fe3c20554d5bee21ed44b9cdc43cde9a53d7cdce)), closes [#66](https://github.com/acdh-oeaw/apis-core-rdf/issues/66)
* **utils:** introduce APIS_ENTITIES settings function ([14fa858](https://github.com/acdh-oeaw/apis-core-rdf/commit/14fa858792ef51af03c2229460fe1a4518a82a86))


### Bug Fixes

* **apis_entities,apis_relations:** drop login_url override ([2f3c6a4](https://github.com/acdh-oeaw/apis-core-rdf/commit/2f3c6a40518c43fb915e2a5e858216a59fa22378))
* **apis_entities:** make relations pagination configurable ([164d9dc](https://github.com/acdh-oeaw/apis-core-rdf/commit/164d9dc02b499d35bda13d509e7050c16a8c713b))
* **apis_metainfo:** rename templatetags ([22b8145](https://github.com/acdh-oeaw/apis-core-rdf/commit/22b814555a91b3a0526bc3a153e16c39352ac978)), closes [#163](https://github.com/acdh-oeaw/apis-core-rdf/issues/163)
* show reference button in detail view ([9120ed2](https://github.com/acdh-oeaw/apis-core-rdf/commit/9120ed20a73b54052544c4effc3110b48172bc13))


### Code Refactoring

* **apis_metainfo:** drop UriCandidate ([8de5061](https://github.com/acdh-oeaw/apis-core-rdf/commit/8de5061bbab0bdcae1c1e735320ca6a9ecc37fa2)), closes [#183](https://github.com/acdh-oeaw/apis-core-rdf/issues/183)

## [0.1.1](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.1.0...v0.1.1) (2023-08-30)


### Bug Fixes

* replace custom duplication logic with signal ([0b1c20d](https://github.com/acdh-oeaw/apis-core-rdf/commit/0b1c20d61aed9d53c6acce90e87e617560f10718))
* use the filter method of the superclass, if it exists ([b96ec9e](https://github.com/acdh-oeaw/apis-core-rdf/commit/b96ec9eb489eaffbec804fa910bf7cb5c47c1fce)), closes [#263](https://github.com/acdh-oeaw/apis-core-rdf/issues/263)

## 0.1.0 (2023-08-28)


### ⚠ BREAKING CHANGES

* **apis_tei:** drop the apis_tei module
* bump Python dependency to >=3.11
* **apis_entities:** this changes the format of the `list_filters` setting of the APIS_ENTITIES setting to a pure dict.
* external projects using functionality from `helper_functions` will have to update their imports.

### Features

* **apis_entities, api_routers:** use access and filter mixins ([47d0cef](https://github.com/acdh-oeaw/apis-core-rdf/commit/47d0cefa500c9ef8b8172aac1c777361da191819))
* **apis_entities,utils:** introduce new tei renderer ([199f2f4](https://github.com/acdh-oeaw/apis-core-rdf/commit/199f2f453dab020f556dcb7c8b6b96e17a96e0d7))
* **apis_entities:** add additional block to generic detail template ([994524c](https://github.com/acdh-oeaw/apis-core-rdf/commit/994524c1e737eb3a2f4a7c7f9b4484baa60ac0d1))
* **apis_entities:** copy fields when merging entities ([66d7c51](https://github.com/acdh-oeaw/apis-core-rdf/commit/66d7c51613ad5de4162da4fbdb8e782b2e9edd10)), closes [#140](https://github.com/acdh-oeaw/apis-core-rdf/issues/140)
* **apis_entities:** filter allowed related types to only allowed ([e374239](https://github.com/acdh-oeaw/apis-core-rdf/commit/e3742395e1e52dea7e0a84e416b9c3b40f720912))
* **apis_entities:** introduce apis_entities.mixins ([5f6c86c](https://github.com/acdh-oeaw/apis-core-rdf/commit/5f6c86c79f483a98d271b8d22819bb861100bb42))
* **apis_entities:** introduce merge_with signal ([844852d](https://github.com/acdh-oeaw/apis-core-rdf/commit/844852dbaf7a18dfb4611d7df6c3ebf25e976033))
* **apis_entities:** let users override the serializer for renderers ([e52fa7f](https://github.com/acdh-oeaw/apis-core-rdf/commit/e52fa7f7045816c36f6822b3326fd5c75b618390))
* **apis_entities:** refactor code and make custom filters possible ([7e0a087](https://github.com/acdh-oeaw/apis-core-rdf/commit/7e0a087e3d00ee6332e6245bc2b61e21f39d2765)), closes [#144](https://github.com/acdh-oeaw/apis-core-rdf/issues/144)
* **apis_metainfo:** introduce an API endpoint for resolving URIs ([461b0eb](https://github.com/acdh-oeaw/apis-core-rdf/commit/461b0eb6b9e15a9a0ce004c8f24154a0d31bc42d))
* **apis_metainfo:** introduce duplication signals ([a54e00e](https://github.com/acdh-oeaw/apis-core-rdf/commit/a54e00e2d4b94229cb4d77c412fdd1bf3ebce2d7))
* **apis_metainfo:** provide a login template ([a8f88f2](https://github.com/acdh-oeaw/apis-core-rdf/commit/a8f88f280ab533d00bf3e9f760ea8749077c7b48)), closes [#210](https://github.com/acdh-oeaw/apis-core-rdf/issues/210)
* **apis_metainfo:** replace fundament with pure bootstrap ([fd7e288](https://github.com/acdh-oeaw/apis-core-rdf/commit/fd7e288efbb77cf7eb9a5ece69cbe5ed8760fd7e)), closes [#180](https://github.com/acdh-oeaw/apis-core-rdf/issues/180)
* **apis_tei:** drop the apis_tei module ([b0bea90](https://github.com/acdh-oeaw/apis-core-rdf/commit/b0bea902cf4507569ab256efaf3082799d6bca9d))
* **core:** Introduce ViewPassesTestMixin and ListViewObjectFilterMixin ([082d798](https://github.com/acdh-oeaw/apis-core-rdf/commit/082d798368fed36aa62fa1da62dd9b860f0816ee))
* implement duplication of RootObject children ([a709639](https://github.com/acdh-oeaw/apis-core-rdf/commit/a70963971896d3d0ba4eb2bc51e68693c47019c9))
* Implement form, view and route for adding URIs ([5a141b6](https://github.com/acdh-oeaw/apis-core-rdf/commit/5a141b6e3d3641f61acd3c9323a577a520f9c084))
* implement new rdf parser ([83ce845](https://github.com/acdh-oeaw/apis-core-rdf/commit/83ce845c73b391f58aadf84033eb396b527d4069))


### Bug Fixes

* add acdh-django-charts dependency ([014da3e](https://github.com/acdh-oeaw/apis-core-rdf/commit/014da3eb1728734f50565fefc5cf998e09767ae1))
* apis_entities: get filter fields from APIS_ENTITIES settings ([a9eb868](https://github.com/acdh-oeaw/apis-core-rdf/commit/a9eb86831c1f180a52b633668b06e09a9afe1c7d))
* apis_entities: template_name should not be prefixed with namespace ([42722f0](https://github.com/acdh-oeaw/apis-core-rdf/commit/42722f04c254da45d683a9cceaf76d4d4b951696))
* apis_entities: use logger instead of an exception ([7f1fcbb](https://github.com/acdh-oeaw/apis-core-rdf/commit/7f1fcbb4d7b13662b9744074877f172ebec3ed1e))
* **apis_entities:** drop django guardian related code and dependency ([8b5f982](https://github.com/acdh-oeaw/apis-core-rdf/commit/8b5f9827bf8047c20de1dad570ca5c41f3817427))
* **apis_entities:** fix transferral of Uris in merge method ([c866a1a](https://github.com/acdh-oeaw/apis-core-rdf/commit/c866a1adda42430650a796e61a3c0b84a55078a3))
* **apis_entities:** remove `merge` column and form ([22f96cf](https://github.com/acdh-oeaw/apis-core-rdf/commit/22f96cf7bd4138f38b32c56542adbf0793429a85)), closes [#168](https://github.com/acdh-oeaw/apis-core-rdf/issues/168)
* **apis_entities:** return uri.root_object instead of uri itself ([abaa1d9](https://github.com/acdh-oeaw/apis-core-rdf/commit/abaa1d96b946e8d843d1ccae443af55717f5fcc2))
* **apis_metainfo:** add zero margin to the usermenu in the navbar ([c35d13b](https://github.com/acdh-oeaw/apis-core-rdf/commit/c35d13bcf026b9946c3ec0eb908b87880a246e02))
* **apis_metainfo:** drop unused api_views module ([d15fa79](https://github.com/acdh-oeaw/apis-core-rdf/commit/d15fa79cd5c9e76612b5bb0aca66ad5186950c19))
* **apis_relations:** fix accidental newline after `if` in template ([b570a8d](https://github.com/acdh-oeaw/apis-core-rdf/commit/b570a8d8101ce8e4ae8a617a01f0924e933cfadb)), closes [#236](https://github.com/acdh-oeaw/apis-core-rdf/issues/236)
* **apis:** show an empty page on `/` instead of an errorpage ([95f97d4](https://github.com/acdh-oeaw/apis-core-rdf/commit/95f97d4153318b92316e2da4f64bc5d99b699bff))
* Changed ContentType.objects.get(model=&lt;MODEL NAME&gt;) to ContentType.objects.get_for_model(<MODEL>) ([7dfa2ac](https://github.com/acdh-oeaw/apis-core-rdf/commit/7dfa2ac1d8ad97584a55f9b5c865e451959971a0))
* cleanup entity_settings vs APIS_SETTINGS ([0bc67a8](https://github.com/acdh-oeaw/apis-core-rdf/commit/0bc67a8771830d0c5c65fd5fda4c0f5d15efa0e6))
* drop legacy RDF parser ([602aebd](https://github.com/acdh-oeaw/apis-core-rdf/commit/602aebdd441ed140cfd58173b0e4a8cc32680371))
* fixes [#117](https://github.com/acdh-oeaw/apis-core-rdf/issues/117) ([8e7a713](https://github.com/acdh-oeaw/apis-core-rdf/commit/8e7a7131c36e227ef98ded51337830cef2b1cdd0))
* harden and enhance Uri model ([d8f26b8](https://github.com/acdh-oeaw/apis-core-rdf/commit/d8f26b833b8255b9ff4049081e761f2b3f9d1af7))
* lowers django version to allow for MariaDB 10.3 ([a8f76f7](https://github.com/acdh-oeaw/apis-core-rdf/commit/a8f76f7b96a292cc4faeb751eb2430bbe4bd9477))
* Set the default_auto_field in all the apps ([69af77f](https://github.com/acdh-oeaw/apis-core-rdf/commit/69af77f23c6208db551040970516882a36ff9a86))
* typo in template ([082ec37](https://github.com/acdh-oeaw/apis-core-rdf/commit/082ec37bd0f5f2f88c8816a647f532f98cfe2df5))
* use the new BASE_TEMPLATE ([ea7936e](https://github.com/acdh-oeaw/apis-core-rdf/commit/ea7936e6266807d88644b5deb05698ffa42257d5))
* **utils:** fix bug and add test case ([a3e9a3a](https://github.com/acdh-oeaw/apis-core-rdf/commit/a3e9a3ae23aa5574307212daaf7814e555670935))
* **utils:** use local files for rdf parser to circument http timeouts ([ce0dd89](https://github.com/acdh-oeaw/apis-core-rdf/commit/ce0dd89bb43327da0034cc51ca3b331fb6450e12)), closes [#174](https://github.com/acdh-oeaw/apis-core-rdf/issues/174)


### Documentation

* Add a workflow that builds and publishes documentation ([bebc4a7](https://github.com/acdh-oeaw/apis-core-rdf/commit/bebc4a76805990eea735288621cdb202acebd6dc)), closes [#67](https://github.com/acdh-oeaw/apis-core-rdf/issues/67)
* Add docs dependencies to pyproject.toml ([912f7a8](https://github.com/acdh-oeaw/apis-core-rdf/commit/912f7a8e60ed21889621ce8f882eb31edefac049))
* add documentation for custom access and list view filter settings ([efa0fea](https://github.com/acdh-oeaw/apis-core-rdf/commit/efa0fea3a78ba7fbc75de5cfbed00352d07254cd))
* add new Makefile and .gitignore ([166f223](https://github.com/acdh-oeaw/apis-core-rdf/commit/166f2238dc325c8cdd75bbe50f03f2fbfca643f5))
* automatically generate module documentation ([6456261](https://github.com/acdh-oeaw/apis-core-rdf/commit/645626179bdb83046ed6f2080353ed23f9ba7d3b))
* Delete stale generated documentation ([1b83caf](https://github.com/acdh-oeaw/apis-core-rdf/commit/1b83caf0d3f07b4e9f7b9a5dd853abbe83c411c6))
* remove stale .doctrees directory ([9582ac2](https://github.com/acdh-oeaw/apis-core-rdf/commit/9582ac292d8eea166a45468868ff687e7f0e27ad))
* Start a glossary ([337ecd5](https://github.com/acdh-oeaw/apis-core-rdf/commit/337ecd5fc06a6b9d5da37038b8c212cfc0fade2f))
* update documentation regarding new entity filters ([f828511](https://github.com/acdh-oeaw/apis-core-rdf/commit/f82851150308ba6bc2a3e7274897fe2f19886ea4))


### Styles

* rename `helper_functions` to `utils` ([0f083d5](https://github.com/acdh-oeaw/apis-core-rdf/commit/0f083d5d17a17b311435b540af0b19368654de20)), closes [#131](https://github.com/acdh-oeaw/apis-core-rdf/issues/131)


### Miscellaneous Chores

* bump Python dependency to &gt;=3.11 ([3a67844](https://github.com/acdh-oeaw/apis-core-rdf/commit/3a67844d357af33e4a344bdb2f21be7d4f00a1ab)), closes [#171](https://github.com/acdh-oeaw/apis-core-rdf/issues/171)
