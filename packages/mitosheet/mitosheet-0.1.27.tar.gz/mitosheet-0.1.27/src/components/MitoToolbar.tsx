// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React from 'react';

// Import CSS
import "../../css/mito-toolbar.css"

// Import Types
import { SheetJSON } from '../widget';
import { ModalEnum } from './Mito';

// Import Components 
import Tooltip from './Tooltip';

const MitoToolbar = (
    props: {
        sheetJSON: SheetJSON, 
        selectedSheetIndex: number,
        send: (msg: Record<string, unknown>) => void,
        setDocumentation: (documentationOpen: boolean) => void,
        selectedCell: string,
        setModal: (modal: ModalEnum) => void,
        model_id: string
    }): JSX.Element => {

    /* Adds a new column onto the end of a sheet, with A, B, C... as the name */
    const addColumn = () => {
        const newColumn = String.fromCharCode(65 + props.sheetJSON.columns.length);
        // Log the new column creation
        window.logger?.track({
            userId: window.user_id,
            event: 'button_column_added_log_event',
            properties: {
                column_header: newColumn
            }
        })
        // TODO: have to update these timestamps, etc to be legit
        props.send({
            'event': 'edit_event',
            'type': 'add_column',
            'sheet_index': props.selectedSheetIndex,
            'id': '123',
            'timestamp': '456',
            'column_header': newColumn
        })
    }

    /* Saves the current file as as an exported analysis */
    const downloadAnalysis = () => {
        window.logger?.track({
            userId: window.user_id,
            event: 'button_download_log_event',
            properties: {}
        })
        // We export using the gridApi.
        window.gridApiMap?.get(props.model_id)?.exportDataAsCsv({
            fileName: 'mito-export'
        });
        props.setModal(ModalEnum.Download);
    }

    const openDocumentation = () => {
        // We log the opening of the repeat documentation sidebar
        window.logger?.track({
            userId: window.user_id,
            event: 'button_documentation_log_event',
            properties: {
                stage: 'opened'
            }
        });
        props.setDocumentation(true);
    }

    const openMerge = () => {
        props.setModal(ModalEnum.Merge);
    }

    return (
        <div className='mito-toolbar-container'>
            <div className='mito-toolbar-item cell-indicator vertical-align-content'>
                <p className="selected-cell">{props.selectedCell}</p>
            </div>

            <button className='mito-toolbar-item vertical-align-content' onClick={addColumn}>
                <svg width="22" height="30" viewBox="0 0 8 12" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M6.45459 1V2.81818" stroke="#343434" strokeWidth="0.7" strokeLinecap="round"/>
                    <path d="M7.36365 1.90909L5.54547 1.90909" stroke="#343434" strokeWidth="0.7" strokeLinecap="round"/>
                    <path d="M6.45455 4.18182V6.90909V10.5455C6.45455 10.7965 6.25104 11 6 11H1.45455C1.20351 11 1 10.7965 1 10.5455V1.45455C1 1.20351 1.20351 1 1.45455 1H4.8961" stroke="#343434" strokeWidth="0.7"/>
                    <rect x="1" y="4.63635" width="5.45455" height="3.63636" fill="#343434" fillOpacity="0.19"/>
                </svg>
                <Tooltip tooltip={"Add Column"}/>
            </button>

            <button className='mito-toolbar-item vertical-align-content' onClick={downloadAnalysis}>
                <svg width="22" height="25" viewBox="0 0 8 9" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M0.899994 5.89999V6.95V8H7.20001V5.89999" stroke="#343434" strokeWidth="0.7" strokeLinecap="round" strokeLinejoin="round"/>
                    <path d="M4.05923 5.39774V0.999997" stroke="#343434" strokeWidth="0.7" strokeLinecap="round"/>
                    <path d="M6.51079 3.88084C6.64455 3.74129 6.63986 3.51974 6.50031 3.38598C6.36077 3.25221 6.13921 3.2569 6.00545 3.39645L6.51079 3.88084ZM4.0905 5.90001L3.8413 6.14577C3.90768 6.21308 3.99846 6.25067 4.09299 6.25C4.18752 6.24933 4.27776 6.21045 4.34317 6.14221L4.0905 5.90001ZM2.10958 3.39288C1.97385 3.25525 1.75225 3.25371 1.61462 3.38944C1.47699 3.52517 1.47545 3.74677 1.61118 3.8844L2.10958 3.39288ZM6.00545 3.39645L3.83783 5.65782L4.34317 6.14221L6.51079 3.88084L6.00545 3.39645ZM4.33971 5.65425L2.10958 3.39288L1.61118 3.8844L3.8413 6.14577L4.33971 5.65425Z" fill="#343434"/>
                </svg>
                <Tooltip tooltip={"Download Analysis"}/>
            </button>

            <button className='mito-toolbar-item' onClick={openDocumentation}>
                <svg width="25" height="25" viewBox="0 0 14 14" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="7" cy="7" r="6.51" stroke="#404040" strokeWidth="0.98"/>
                    <path d="M7.27173 8.43865C7.2624 8.34531 7.2624 8.30798 7.2624 8.26131C7.2624 7.89731 7.38373 7.56131 7.67307 7.36531L8.1024 7.07598C8.64373 6.71198 9.0544 6.19865 9.0544 5.45198C9.0544 4.49998 8.31707 3.57598 7.0104 3.57598C5.57307 3.57598 4.94773 4.63065 4.94773 5.48931C4.94773 5.65731 4.9664 5.80665 5.00373 5.93731L5.90907 6.04931C5.87173 5.94665 5.84373 5.75065 5.84373 5.59198C5.84373 5.00398 6.1984 4.39731 7.0104 4.39731C7.75707 4.39731 8.12107 4.91065 8.12107 5.46131C8.12107 5.82531 7.94373 6.16131 7.6264 6.37598L7.21573 6.65598C6.66507 7.02931 6.44107 7.49598 6.44107 8.11198C6.44107 8.23331 6.44107 8.32665 6.4504 8.43865H7.27173ZM6.24507 9.77331C6.24507 10.1093 6.51573 10.38 6.85173 10.38C7.18773 10.38 7.46773 10.1093 7.46773 9.77331C7.46773 9.43731 7.18773 9.15731 6.85173 9.15731C6.51573 9.15731 6.24507 9.43731 6.24507 9.77331Z" fill="#343434"/>
                </svg>
                <Tooltip tooltip={"Documentation"}/>
            </button>

            <button className='mito-toolbar-item' onClick={openMerge}>
            <svg width="40" height="30" viewBox="0 0 23 13" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M14.705 6.5C14.705 9.83244 11.5513 12.625 7.54 12.625C3.52871 12.625 0.375 9.83244 0.375 6.5C0.375 3.16756 3.52871 0.375 7.54 0.375C11.5513 0.375 14.705 3.16756 14.705 6.5Z" fill="#C8C8C8" stroke="#343434" strokeWidth="0.75"/>
                <path d="M21.9845 6.5C21.9845 9.83244 18.8308 12.625 14.8195 12.625C10.8083 12.625 7.65454 9.83244 7.65454 6.5C7.65454 3.16756 10.8083 0.375 14.8195 0.375C18.8308 0.375 21.9845 3.16756 21.9845 6.5Z" stroke="#343434" strokeWidth="0.75"/>
            </svg>
                <Tooltip tooltip={"Merge"}/>
            </button>
            {/* add className mito-toolbar-item to a div below to add another toolbar item! */}
        </div>
    );
};

export default MitoToolbar;