// Distributed under the terms of the Modified BSD License.

import { Application, IPlugin } from '@phosphor/application';

import { Widget } from '@phosphor/widgets';

import {DOMWidgetView, IJupyterWidgetRegistry, WidgetView} from '@jupyter-widgets/base';

import {INotebookTracker} from "@jupyterlab/notebook";

import {ActiveNotebookModel} from './widget';

import { MODULE_NAME, MODULE_VERSION } from './version';

const EXTENSION_ID = 'dapla-jupyterlab-widgets:plugin';

/**
 * The ActiveNotebook plugin.
 */
const activeNotebookPlugin: IPlugin<Application<Widget>, void> = ({
  id: EXTENSION_ID,
  requires: [IJupyterWidgetRegistry, INotebookTracker],
  activate: activateWidgetExtension,
  autoStart: true,
} as unknown) as IPlugin<Application<Widget>, void>;
// the "as unknown as ..." typecast above is solely to support JupyterLab 1
// and 2 in the same codebase and should be removed when we migrate to Lumino.

export default activeNotebookPlugin;

/**
 * Activate the widget extension.
 */
function activateWidgetExtension(
  app: Application<Widget>,
  registry: IJupyterWidgetRegistry,
  tracker: INotebookTracker
): void {
  let widgetTitle = ''
  tracker.currentChanged.connect(() => {
    if (tracker.currentWidget != null) {
      widgetTitle = tracker.currentWidget.title.label;
      console.log("Setting tracker value " + widgetTitle)
    }
  })

  let ActiveNotebookView = class extends DOMWidgetView {
    initialize(parameters: WidgetView.InitializeParameters) {
      console.log("ExampleView initialized")
      super.initialize(parameters);
      this.model.set('title', widgetTitle);
      this.model.save_changes()
    }
    render() {
      console.log('init ActiveNotebookView')
    }
  }

  registry.registerWidget({
    name: MODULE_NAME,
    version: MODULE_VERSION,
    exports: {
      ActiveNotebookModel: ActiveNotebookModel,
      ActiveNotebookView: ActiveNotebookView
    },
  });
}
