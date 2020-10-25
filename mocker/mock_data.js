const faker = require("faker");
const sampleSize = require("lodash.samplesize");
const mysql = require("mysql2/promise");

// Constants for mock generation
const LANGUAGES = ["JavaScript", "Python", "C", "C++", "Java"];
const HOURLY_RATE = [25, 30, 35, 40, 45, 50, 55, 60];
const MEMBER_ROLE = [
    "frontend",
    "backend",
    "fullstack",
    "devops",
    "data",
    "PM",
    "lead",
];
const SKILL_SCORE = [50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100];
const AVAILABLE_HOURS = [10, 20, 40];
const BUDGET = [1000, 5000, 20000, 50000, 100000];
const WEIGHTS = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100];


const numMembers = 5;
const numProjects = 3;

main();

async function main() {
    // establish mysql server connection
    const connection = await mysql.createConnection({
        host: "database",
        port: "3306",
        database: "teamformationassistant",
        user: "dbuser",
        password: "dbuserpwd",
        multipleStatements: true,
    }).catch((err) => {
        console.log(err)
    });

    // Generate and insert mock members
    for (let i = 0; i < numMembers; i++) {
        let member = generateMockMember();
        let memberQuery =
            "INSERT INTO Member (MemberName, DOB, Languages, IsAssigned, HourlyRate, MemberRole, Experience, SkillScore, AvailableHoursPerWeek) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);";
        connection.query(memberQuery, Object.values(member));
    }

    // Generate mock projects and requirements
    for (let i = 0; i < numProjects; i++) {
        let project = generateMockProject();

        let projectQuery =
            "INSERT INTO Project (ProjectName, ProjectEndDate, ProjectTeamSize, Budget, Tools, IsAssignmentComplete, Priority) VALUES(?, ?, ?, ?, ?, ?, ?);";
        await connection.query(projectQuery, Object.values(project));

        let projectIdQuery =
            "SELECT ProjectId FROM Project WHERE ProjectName = ?;";
        let [rows, fields] = await connection.query(
            projectIdQuery,
            project.ProjectName
        );
        let projectId = rows[0].ProjectId;

        for (let j = 0; j < project.ProjectTeamSize; j++) {
            let requirement = generateMockRequirements();

            let requirementQuery =
                "INSERT INTO Requirements (ProjectId, LanguagePreferred, Skill, MemberRole, AvailableHoursPerWeek, SkillWeight, ExperienceWeight, HoursWeight, LanguageWeight, BudgetWeight) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);";
            let values = Object.values(requirement);
            values.unshift(projectId);
            connection.query(requirementQuery, values);
        }
    }

    // console.log(projects);
    connection.end();
}

// Generate a mock member
function generateMockMember() {
    return {
        MemberName: faker.name.findName(),
        DOB: formatDate(faker.date.between("2000-01-01", "1980-01-01")),
        Languages: sampleSize(LANGUAGES, getRandomInt(2, 5)).join(","),
        IsAssigned: 0,
        HourlyRate: sampleSize(HOURLY_RATE),
        MemberRole: sampleSize(MEMBER_ROLE),
        Experience: getRandomInt(0, 20),
        SkillScore: sampleSize(SKILL_SCORE),
        AvailableHoursPerWeek: sampleSize(AVAILABLE_HOURS),
    };
}

// Generate a mock project
function generateMockProject() {
    return {
        ProjectName: faker.company.companyName(),
        ProjectEndDate: formatDate(faker.date.future(4)),
        ProjectTeamSize: getRandomInt(2, 6),
        Budget: sampleSize(BUDGET),
        Tools: "",
        IsAssignmentComplete: 0,
        Priority: getRandomInt(0, 4),
    };
}

// Generate a mock requirement
function generateMockRequirements() {
    let temp = sampleSize(WEIGHTS, 4);
    temp.push(0);
    temp.push(100);
    temp.sort((a, b) => a - b);

    let weights = [];
    for (let i = 0; i < temp.length - 1; i++) {
        let a = temp[i];
        let b = temp[i + 1];
        weights.push(b - a);
    }

    return {
        LanguagePreferred: sampleSize(LANGUAGES, getRandomInt(2, 5)).join(","),
        Skill: sampleSize(SKILL_SCORE),
        MemberRole: sampleSize(MEMBER_ROLE),
        AvailableHoursPerWeek: sampleSize(AVAILABLE_HOURS),
        SkillWeight: weights[0],
        ExperienceWeight: weights[1],
        HoursWeight: weights[2],
        LanguageWeight: weights[3],
        BudgetWeight: weights[4],
    };
}

// Get random int between min and max (inclusive)
function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

// Format a date object into a string
function formatDate(date) {
    let month = "" + (date.getMonth() + 1);
    let day = "" + date.getDate();
    let year = date.getFullYear();

    if (month.length < 2) {
        month = "0" + month;
    }

    if (day.length < 2) {
        day = "0" + day;
    }

    return [year, month, day].join("-");
}
