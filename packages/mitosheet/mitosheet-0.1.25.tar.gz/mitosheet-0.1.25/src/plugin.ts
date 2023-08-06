// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import { Application, IPlugin } from '@phosphor/application';

import { Widget } from '@phosphor/widgets';

import { IJupyterWidgetRegistry } from '@jupyter-widgets/base';

import {
  INotebookTracker, NotebookActions
} from '@jupyterlab/notebook';

import {
  ICellModel
} from "@jupyterlab/cells";

import * as widgetExports from './widget';
import { ColumnSpreadsheetCodeJSON } from './components/Mito';

import { MODULE_NAME, MODULE_VERSION } from './version';

import {
  IObservableString,
  IObservableUndoableList
} from '@jupyterlab/observables';
import { SheetJSON } from './widget';

const EXTENSION_ID = 'mitosheet:plugin';

/**
 * The example plugin.
 */
const examplePlugin: IPlugin<Application<Widget>, void> = ({
  id: EXTENSION_ID,
  requires: [IJupyterWidgetRegistry, INotebookTracker],
  activate: activateWidgetExtension,
  autoStart: true,
} as unknown) as IPlugin<Application<Widget>, void>;
// the "as unknown as ..." typecast above is solely to support JupyterLab 1
// and 2 in the same codebase and should be removed when we migrate to Lumino.

export default examplePlugin;


function getCellAtIndex(cells: IObservableUndoableList<ICellModel> | undefined, index: number): ICellModel | undefined {
  if (cells == undefined) {
    return undefined;
  }

  const cellsIterator = cells.iter();
  let cell = cellsIterator.next();
  let i = 0;
  while (cell) {
    if (i == index) {
      return cell;
    }

    i++;
    cell = cellsIterator.next();
  }

  
  return undefined;
}

function codeContainer(
    imports: string, 
    code: string[], 
    dfNames: string[], 
    columnSpreadsheetCodeJSONArray: ColumnSpreadsheetCodeJSON[],
    numberedDfString: string
  ): string {

  // This is the parameters in the mito_analysis function definition
  const functionDefParams = dfNames.map((dfName, idx) => {
    return `df${idx + 1}`
  }).join(', ');
  // And these are the actual variables to call the call to the mito_analysis function
  const functionCallParams =  dfNames.join(', ');

  return `# MITO CODE START (DO NOT EDIT)
# SAVED-ANALYSIS-START${JSON.stringify(columnSpreadsheetCodeJSONArray)}SAVED-ANALYSIS-END

${imports}

def mito_analysis(${functionDefParams}):
    ${code.join("\n\n    ")}

    return ${numberedDfString}


${numberedDfString} = mito_analysis(${functionCallParams})
  
# MITO CODE END (DO NOT EDIT)`
}


function getColumnSpreadsheetCodeJSONArray(codeblock: string): ColumnSpreadsheetCodeJSON[] | undefined {
  /*
    Given the above code container format, returns the columnSpreadsheetCodeJSON
    that was saved above. 

    Returns undefined if this does not exist; this will happen when no mito analysis 
    exists in the codeblock.
  */

  if (!codeblock.includes('SAVED-ANALYSIS-START')) {
    return undefined;
  }

  // We get just the string part of the container that is the column spreadsheet code
  const columnSpreadsheetCodeJSONString = codeblock.substring(
    codeblock.indexOf('SAVED-ANALYSIS-START') + 'SAVED-ANALYSIS-START'.length,
    codeblock.indexOf('SAVED-ANALYSIS-END')
  )

  return JSON.parse(columnSpreadsheetCodeJSONString) as ColumnSpreadsheetCodeJSON[];
}



/**
 * Activate the widget extension.
 */
function activateWidgetExtension(
  app: Application<Widget>,
  registry: IJupyterWidgetRegistry,
  tracker: INotebookTracker
): void {

  /*
    We define a command here, so that we can call it elsewhere in the
    app - and here is the only place we have access to the app (which we
    need to be able to add commands) and tracker (which we need to get
    the current notebook).
  */
  app.commands.addCommand('write-code-to-cell', {
    label: 'Write Mito Code to a Cell',
    execute: (args: any) => {
      const dfNames = args.dfNames as string[];
      const codeJSON = args.codeJSON as widgetExports.CodeJSON;
      const columnSpreadsheetCodeJSONArray = args.columnSpreadsheetCodeJSONArray as ColumnSpreadsheetCodeJSON[];
      const sheetJSONArray = args.sheetJSONArray as SheetJSON[];

      // Build a string of the form: 'df1, df2, df3 ... ', which we use in the code container
      // and elsewhere in the codeblock
      const numberedDfString = sheetJSONArray.map((sheetJSON, index) => {
        return `df${index + 1}`
      }).join(', ');
      
      // This is the code that was passed to write to the cell.
      const code = codeContainer(codeJSON.imports, codeJSON.code, dfNames, columnSpreadsheetCodeJSONArray, numberedDfString);

      // We get the current notebook (currentWidget)
      const notebook = tracker.currentWidget?.content;
      if (notebook) {
        // Then, we cell if this is the cell that is actually displaying the mito sheet
        const activeCell = notebook.activeCell;
        if (activeCell) {
          /*
            TODO: we need to fix all the bugs that arise because of the assumption 
            that the cell displaying the sheet actually contains the init call...

            Note we don't continue if it doesn't contain a mito sheet call, or 
            if it's the repeated analysis cell.
          */
          const value = activeCell.model.modelDB.get('value') as IObservableString;
          const currentCode = value.text;
          if (!currentCode.includes('mitosheet.sheet')) {
            return
          }
          /*
            Algorithm below:
            1. Figure out if we've already written Mito code, and if so just replace it
            2. If we haven't written code, then:
              a) Split the existing code at the last line (that displays the sheet)
              b) Put the code in the middle of this
          */

          if (currentCode.includes('MITO CODE')) {
            const preamble = currentCode.substring(0, currentCode.indexOf("# MITO CODE START"));
            let postamble = currentCode.substring(
              currentCode.indexOf("MITO CODE END") + "MITO CODE END (DO NOT EDIT)".length
            );

            // We keep all the code _before_ the mitosheet.sheet call, but replace
            // the parameters to the mitosheet.sheet call with our own 
            const prefixPosition = postamble.indexOf('mitosheet.sheet(')
            postamble = postamble.substring(0, prefixPosition)
            postamble += `mitosheet.sheet(${numberedDfString})`

            const newCode = preamble + code + postamble;
            value.text = newCode;
          } else {
            const lines = currentCode.split('\n');
            let displayLine = '';
            let i = lines.length - 1
            for (i; i >= 0; i--) {
              // Find the last non-whitespace line
              const currentLine = lines[i].trim();
              if (currentLine.length > 0) {
                displayLine = currentLine;
                break;
              }
            }

            // As above, we keep the code before the mitosheet.sheet call, but replace
            // the params with our own.
            const prefixPosition = displayLine.indexOf('mitosheet.sheet(')
            displayLine = displayLine.substring(0, prefixPosition)
            displayLine += `mitosheet.sheet(${numberedDfString})`

            // We rejoin all the lines that aren't the last line
            const preamble = lines.slice(0, i).join('\n');
            const newCode = `${preamble}\n\n${code}\n\n${displayLine}`;
            value.text = newCode;
          }
        }
      }
    }
  });


  app.commands.addCommand('repeat-analysis', {
    label: 'Replicates the current analysis on a given new file, in a new cell.',
    execute: (args: any) => {

      const fileName = args.fileName as string;

      // We get the current notebook (currentWidget)
      const notebook = tracker.currentWidget?.content;
      const context = tracker.currentWidget?.context;
      if (!notebook || !context) return;

      // We run the current cell and insert a cell below
      NotebookActions.runAndInsert(notebook, context.sessionContext);

      // And then we write to this inserted cell (which is now the active cell)
      const activeCell = notebook.activeCell;
      if (activeCell) {
        const value = activeCell.model.modelDB.get('value') as IObservableString;
        const df_name = fileName.replace(' ', '_').split('.')[0]; // We replace common file names with a dataframe name
        const code = `# Repeated analysis on ${fileName}\n\n${df_name} = pd.read_csv(\'${fileName}\')\n\nmito_analysis(${df_name})\n\nmitosheet.sheet(${df_name})`
        value.text = code;
      }
    }
  });

  app.commands.addCommand('get-df-names', {
    label: 'Read df name from mitosheet.sheet call',
    execute: (args) : string[] => {
      /*
        This function has to deal with the fact that there are 2 cases
        in which we want to get the dataframe names:
        1. The first time we are rendering a mitosheet (e.g. after you run a sheet
          with a mitosheet.sheet call).
          
          In this case, the active cell is the cell _after_ the mitosheet.sheet call.

        2. When you have a Mito sheet already displayed and saved in your notebook, 
          and your refresh the page. 

          In this case, the active cell is the first cell in the notebook, which
          may or may not be the cell the mitosheet.sheet call is actually made. 

        We handle these cases by detecting which case we're in based on the index
        of the currently selected cell. 

        However, in a sheet with _multiple_ mitosheet.sheet calls, if we're in
        case (2), we can't know which cell to pull from. I haven't been able to
        think of away around this. 
        
        However, since this is rare for now, we don't worry about it and just do whatever
        here for now, and hope the user will refresh the sheet if it's not working!
      */

      // We get the current notebook (currentWidget)
      const notebook = tracker.currentWidget?.content;

      if (!notebook) return [];

      const activeCellIndex = notebook.activeCellIndex;
      const cells = notebook.model?.cells;

      const getDfNamesFromCellContent = (content: string): string[] => {
        const nameString = content.split('mitosheet.sheet(')[1].split(')')[0];
        return nameString.split(',').map(dfName => dfName.trim());
      }

      // See comment above. We are in case (2). 
      if (activeCellIndex === 0 && cells !== undefined) {
        // We just get the first mitosheet.sheet call we can find

        const cellsIterator = cells.iter();
        let cell = cellsIterator.next();
        while (cell) {
          const cellContent = (cell.modelDB.get('value') as IObservableString).text;
          if (cellContent.includes('mitosheet.sheet')) {
            return getDfNamesFromCellContent(cellContent);
          }
          cell = cellsIterator.next();
        }
        return [];
      } else {
        // Otherwise, were in case (1)
        const previousCell = getCellAtIndex(cells, activeCellIndex - 1); // TODO: change this to next cell model or something
        if (previousCell) {
          // remove the df argument to mitosheet.sheet() from the cell's text
          const previousCellContent = (previousCell.modelDB.get('value') as IObservableString).text;
          return getDfNamesFromCellContent(previousCellContent);
        }
        return [];
      }      
    }
  });

  app.commands.addCommand('read-existing-analysis', {
    label: 'Reads any existing mito analysis from the previous cell, and returns the saved ColumnSpreadsheetCodeJSON, if it exists.',
    execute: (args: any): ColumnSpreadsheetCodeJSON[] | undefined => {

      // We get the current notebook (currentWidget)
      const notebook = tracker.currentWidget?.content;

      if (!notebook) return undefined;

      // We get the previous cell to the current active cell
      const activeCellIndex = notebook.activeCellIndex;
      const cells = notebook.model?.cells;
      const previousCell = getCellAtIndex(cells, activeCellIndex - 1);

      // We read it's string in, and get 

      if (previousCell) {
        // remove the df argument to mitosheet.sheet() from the cell's text
        const previousValue = previousCell.modelDB.get('value') as IObservableString;
        return getColumnSpreadsheetCodeJSONArray(previousValue.text);
      } 
      return undefined;
    }
  });

  window.commands = app.commands; // so we can write to it elsewhere
  registry.registerWidget({
    name: MODULE_NAME,
    version: MODULE_VERSION,
    exports: widgetExports,
  });
}


