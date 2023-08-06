// Distributed under the terms of the Modified BSD License.

import {
  DOMWidgetModel,
  ISerializers,
} from '@jupyter-widgets/base';

import { MODULE_NAME, MODULE_VERSION } from './version';

export class ActiveNotebookModel extends DOMWidgetModel {
  defaults() {
    console.log('init ActiveNotebookModel')
    return {
      ...super.defaults(),
      _model_name: ActiveNotebookModel.model_name,
      _model_module: ActiveNotebookModel.model_module,
      _model_module_version: ActiveNotebookModel.model_module_version,
      _view_name: ActiveNotebookModel.view_name,
      _view_module: ActiveNotebookModel.view_module,
      _view_module_version: ActiveNotebookModel.view_module_version,
      title: '',
    };
  }

  initialize(attributes: any, options: any) {
    super.initialize(attributes, options);
    this.widget_manager.display_model(undefined as any, this, {});
  }

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers,
    // Add any extra serializers here
  };

  static model_name = 'ActiveNotebookModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'ActiveNotebookView'; // Set to null if no view
  static view_module = MODULE_NAME; // Set to null if no view
  static view_module_version = MODULE_VERSION;
}
