// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, { FormEvent } from 'react';

// Import types
import { CellFocusedEvent } from 'ag-grid-community';
import { SheetJSON, ErrorJSON } from '../widget';

// Import sheet and code components
import MitoSheet from './MitoSheet';
import SheetTab from './SheetTab';
import FormulaBar from './FormulaBar';
import MitoToolbar from './MitoToolbar';
import DocumentationSidebar from './DocumentationSidebar';

// Import modals
import ErrorModal from './ErrorModal';
import DownloadModal from './DownloadModal';
import RepeatAnalysisModal from './RepeatAnalysisModal';
import MergeModal from './MergeModal';

// Import css
import "../../css/mito.css"

export interface ColumnSpreadsheetCodeJSON {
    [Key: string]: string;
}

type MitoProps = {
    dfNames: string[];
    columnSpreadsheetCodeJSONArray: ColumnSpreadsheetCodeJSON[];
    sheetJSONArray: SheetJSON[];
    send: (msg: Record<string, unknown>) => void
    model_id: string;
};

type MitoState = {
    dfNames: string[];
    columnSpreadsheetCodeJSONArray: ColumnSpreadsheetCodeJSON[];
    sheetJSONArray: SheetJSON[];
    selectedSheetIndex: number;
    formulaBarValue: string;
    selectedColumn: string;
    selectedRowIndex: number;
    errorJSON: ErrorJSON;
    editingCellColumn : string;
    editingCellRowIndex : number;
    documentationOpen: boolean;
    modal: ModalEnum;
};

const INDEX_COLUMN = "index";


export enum ModalEnum {
    None = 'None',
    Error = 'Error',
    RepeatAnalysis = 'RepeatAnalysis',
    Download = 'Download',
    Merge = 'Merge'
}


class Mito extends React.Component<MitoProps, MitoState> {

    constructor(props: MitoProps) {
        super(props);

        this.state = {
            dfNames: this.props.dfNames,
            columnSpreadsheetCodeJSONArray: this.props.columnSpreadsheetCodeJSONArray,
            sheetJSONArray: this.props.sheetJSONArray,
            selectedSheetIndex: 0,
            formulaBarValue: this.props.sheetJSONArray[0].data[0][0],
            selectedColumn: this.props.sheetJSONArray[0].columns[0].toString(),
            selectedRowIndex: 0,
            /*
                note that editingCellColumn and editingCellRowIndex should both either
                be set to these default values or they should be set to valid cell values

                If they are these default values, we are not editing a cell, and otherwise
                we are editing the cell they are set to!
            */
            editingCellColumn: "",
            editingCellRowIndex: -1,
            documentationOpen: false,
            modal: ModalEnum.None,
            errorJSON: {
                event: '',
                type: '',
                header: '',
                to_fix: ''
            }
        };

        this.cellFocused = this.cellFocused.bind(this);
        this.handleFormulaBarEdit = this.handleFormulaBarEdit.bind(this);
        this.handleFormulaBarSubmit = this.handleFormulaBarSubmit.bind(this);
        this.sendCellValueUpdate = this.sendCellValueUpdate.bind(this);
        this.setEditingMode = this.setEditingMode.bind(this);
        this.setDocumentation = this.setDocumentation.bind(this);
        this.setModal = this.setModal.bind(this);
        this.getCurrentModalComponent = this.getCurrentModalComponent.bind(this);
        this.setSelectedSheetIndex = this.setSelectedSheetIndex.bind(this);
    }

    /* 
        This function is responsible for turning cell editing mode on and off
        by setting the state of editingCellColumn, and editingCellRowIndex.

        If you call this function with on===true, then the passed column and rowIndex
        should be the cell you want to start editing.

        If you call this function with on==false, then editing will be stopped, and the 
        passed column and rowIndex will be focused on.
    */
    setEditingMode(on: boolean, column: string, rowIndex: number) : void {
        if (on && this.state.editingCellRowIndex === -1) {
            /* 
                This runs (and turns on editing mode) when we're not in editing mode and:
                1. The user double clicks on a cell
                2. The user presses enter on a cell. 
                3. The user types any character on a cell. 
            */
            this.setState({
                editingCellColumn: column,
                editingCellRowIndex: rowIndex
            });
        } else if (!on) {
            /* 
                We turn off cell-editing mode and select the given cell.

                This handles some of the many ways cell editing can be stopped
                explicitly (e.g. ENTER), as we want only sometimes want ENTER to stop 
                editing (in other cases, we want it to select a suggestion!).

                To see a list of events that stop editing, see:
                https://www.ag-grid.com/javascript-grid-cell-editing/#stop-end-editing
            */
            this.setState({
                editingCellColumn: "",
                editingCellRowIndex: -1
            });

            // We actually stop the grid from editing in this case, and set cell focus
            // as stopping editing focuses on nothing by default.
            window.gridApiMap?.get(this.props.model_id)?.stopEditing();
            window.gridApiMap?.get(this.props.model_id)?.setFocusedCell(
                rowIndex, 
                column
            );
        }
    }

    /* 
        Occurs when a cell is clicked. If we are currently editing a cell, we append the clicked
        column to the currently-edited cell. Otherwise, we select the clicked cell.
    */
    cellFocused(event : CellFocusedEvent) : void {
        /* 
            We avoid cell focused throwing an error when switching sheets by making sure the 
            event is defined, and just returning. Not sure why this occurs!
        */
        const column = event.column?.getColId();
        if (!column) return;

        if (this.state.editingCellRowIndex !== -1) {
            /* 
                If we're in editing mode, append the clicked column to the currently edited cell;
                We hack this by passing this info through charPress!
            */
            const selectedColumn = JSON.stringify({selectedColumn:column})

            /*  
                turn on the correct cell editor. see extensive comment in MitoCellEditor.tsx 
                constructor about hacking CharPress
            */
            const editingModeParams = {
                rowIndex: this.state.editingCellRowIndex,
                colKey: this.state.editingCellColumn,
                charPress: selectedColumn
            }

            // turn the editing cell's cell editor back on!
            window.gridApiMap?.get(this.props.model_id)?.startEditingCell(editingModeParams);
        } else {
            // If we're not in editing mode, then we update the formula bar only

            // if the column is the index column, then we reset the selected cell state
            if (column === INDEX_COLUMN) {
                this.setState({
                    selectedColumn: '',
                    selectedRowIndex: 0,
                    formulaBarValue: ''
                });
                return;
            }

            // otherwise, get the cell's formula to display
            const columnIndex = this.state.sheetJSONArray[this.state.selectedSheetIndex].columns.indexOf(column);
            const rowIndex = event.rowIndex;

            const columnFormula = this.state.columnSpreadsheetCodeJSONArray[this.state.selectedSheetIndex][column];
            let formulaBarValue = '';
            if (columnFormula !== '') {
                // if the cell has a formula, display it in the formula bar
                formulaBarValue = columnFormula

            } else {
                // otherwise display the value in the formula bar
                formulaBarValue = this.state.sheetJSONArray[this.state.selectedSheetIndex].data[rowIndex][columnIndex];
            }
            
            this.setState({
                selectedColumn: column,
                selectedRowIndex: rowIndex,
                formulaBarValue: formulaBarValue
            });
        }
    }

    handleFormulaBarEdit(e: FormEvent<HTMLInputElement>) : void {
        this.setState({
            formulaBarValue: e.currentTarget.value
        });
    }

    // TODO: do we want a different type of edit for a value change and a formula change or will 
    // we just detect that in the backend and apply the correct edit rules?
    handleFormulaBarSubmit(e : React.FormEvent<HTMLFormElement>) : void {
        e.preventDefault();
        this.sendCellValueUpdate(this.state.selectedColumn, this.state.formulaBarValue);
    }

    // TODO: this event should be broken out into a formula edit and a value edit
    sendCellValueUpdate(column : string, newValue : string) : void {
        /*
            We don't send the formula to the evaluator while in cell editing mode
            because this function gets called after the CellValueChangedEvent fires 
            each time the cell editor is closed. 
            
            However, the cell editor closes each time the user uses their mouse 
            to reference another column - which isn't a finished update yet!
        */
        if (this.state.editingCellRowIndex === -1) {
            this.props.send({
                'event': 'edit_event',
                'type': 'cell_edit',
                'sheet_index': this.state.selectedSheetIndex,
                'id': '123',
                'timestamp': '456',
                'address': column,
                'new_formula': newValue
            });
        }
    }

    setDocumentation(documentationOpen: boolean) : void {
        this.setState({documentationOpen: documentationOpen});
    }

    getCurrentModalComponent(): JSX.Element {
        // Returns the JSX.element that is currently, open, and is used
        // in render to display this modal
        switch(this.state.modal) {
            case ModalEnum.None: return <div></div>;
            case ModalEnum.Error: return (
                <ErrorModal
                    errorJSON={this.state.errorJSON}
                    setModal={this.setModal}
                    />
            )
            case ModalEnum.RepeatAnalysis: return (
                <RepeatAnalysisModal
                    setModal={this.setModal}
                    />
            )
            case ModalEnum.Download: return (
                <DownloadModal
                    setModal={this.setModal}
                    />
            )
            case ModalEnum.Merge: return (
                <MergeModal
                    setModal={this.setModal}
                    sheetJSONArray={this.state.sheetJSONArray}
                    dfNames={this.state.dfNames}
                    send={this.props.send}
                    />
            )
        }
    }

    setModal(modal: ModalEnum) : void {
        this.setState({
            'modal': modal
        });
    }

    setSelectedSheetIndex(newIndex: number): void {
        this.setState({selectedSheetIndex: newIndex});
    }

    // eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
    render() {
        // set the selected cell for the cell indicator in the mito toolbar
        const selectedCell = this.state.selectedColumn + (this.state.selectedRowIndex + 1).toString()
                            
        return (
            <div className="mito-container">
                <div className="mitosheet">
                    <MitoToolbar 
                        sheetJSON={this.state.sheetJSONArray[this.state.selectedSheetIndex]} 
                        selectedSheetIndex={this.state.selectedSheetIndex}
                        selectedCell={selectedCell}
                        send={this.props.send}
                        setDocumentation={this.setDocumentation}
                        setModal={this.setModal}
                        model_id={this.props.model_id}
                        />
                    <FormulaBar
                        formulaBarValue={this.state.formulaBarValue}
                        handleFormulaBarEdit={this.handleFormulaBarEdit}
                        handleFormulaBarSubmit={this.handleFormulaBarSubmit} 
                    />
                    <MitoSheet 
                        sheetJSON={this.state.sheetJSONArray[this.state.selectedSheetIndex]} 
                        setEditingMode={this.setEditingMode}
                        cellFocused={this.cellFocused}
                        model_id={this.props.model_id}
                        sendCellValueUpdate={this.sendCellValueUpdate} 
                        />
                    <div className="sheet-tab-bar">
                        {this.state.sheetJSONArray.map((sheetJSON, index) => {
                            // If we can't get the df name, we just call it Sheet{index}!
                            const sheetName = this.state.dfNames[index] ? this.state.dfNames[index] : `Sheet${index + 1}`
                            return (
                                <SheetTab 
                                    key={sheetName}
                                    sheetName={sheetName}
                                    sheetIndex={index}
                                    selectedSheetIndex={this.state.selectedSheetIndex}
                                    setSelectedSheetIndex={this.setSelectedSheetIndex} />
                            )
                        })}
                    </div>
                </div>
                {this.getCurrentModalComponent()}
                {this.state.documentationOpen && 
                    <div className="sidebar">
                        <DocumentationSidebar setDocumentation={this.setDocumentation}/>
                    </div>
                }                
            </div>
        );
    }

}


export default Mito;