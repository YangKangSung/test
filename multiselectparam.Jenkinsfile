pipeline {
    agent any
    stages {
        stage('Parameters') {
            steps {
                script {
                    properties([
                            parameters([
                                    multiselect(
                                            decisionTree: [
                                                    variableDescriptions: [
                                                            [
                                                                    label       : 'Sport',
                                                                    variableName: 'SELECTED_SPORT'
                                                            ],
                                                            [
                                                                    label       : 'Team',
                                                                    variableName: 'SELECTED_TEAM'
                                                            ]
                                                    ],
                                                    itemList: [
                                                            [children: [
                                                                    [value: 'Tennisclub Rumeln-Kaldenhausen e. V.'],
                                                                    [label: 'Alternative label', value: 'Oppumer TC']
                                                                 ],
                                                             value   : 'Tennis'
                                                            ],
                                                            [children: [
                                                                    [value: 'Rumelner TV'],
                                                                    [value: 'FC Rumeln']
                                                                 ],
                                                             value   : 'Football'],
                                                            [children: [
                                                                    [value: 'WSC Duisburg Rheinhausen']
                                                                 ],
                                                             value   : 'Wakeboard']
                                                    ]
                                            ],
                                            description: 'Please select your favourite team!',
                                            name: 'Favourite team'
                                    )
                            ])
                    ])
                }
            }
        }

        stage('Print variables') {
            steps {
                sh 'set'
                sh 'sleep 30'
            }
        }
    }
}
